import logging
import psycopg2
import re

from odoo import api, models
from odoo.osv import expression
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _search_display_name(self, operator, value):
        search_fnames = self._get_display_name_field_paths()
        if not search_fnames:
            return super()._search_display_name(operator, value)

        # Copied from ORM models.py
        if operator.endswith('like') and not value and '=' not in operator:
            # optimize out the default criterion of ``like ''`` that matches everything
            # return all when operator is positive
            return expression.FALSE_DOMAIN if operator in expression.NEGATIVE_TERM_OPERATORS else expression.TRUE_DOMAIN
        aggregator = expression.AND if operator in expression.NEGATIVE_TERM_OPERATORS else expression.OR
        return aggregator([[(field_name, operator, value)] for field_name in search_fnames])
    
    @api.depends(lambda self: self._get_display_name_field_paths())
    def _compute_display_name(self):

        def get_nested_value_and_field_type(record, field_path):
            """
            Retrieve a nested value from the record using dot notation.
            """
            fields = field_path.split(".")
            value = record
            for field in fields:
                field_type = value._fields.get(field).type
                value = getattr(value, field)
            return (value, field_type)
        
        res = super()._compute_display_name()

        Model = self.env["ir.model"]
        # Order by a field which always exists, to install apps without errors.
        model = Model.sudo().search([("model", "=", self._name)], order="id")

        pattern = model._get_display_name_pattern()
        if not pattern:
            return res

        field_paths = model._get_display_name_field_paths()
        if not field_paths:
            return res

        for record in self:
            # Collect values and types for the field paths
            vals_types = {}
            for field_path in field_paths:
                value_type = get_nested_value_and_field_type(record, field_path)
                vals_types[field_path] = value_type

            # Skip if not all fields have values (don't check boolean fields)
            has_non_boolean_false_value = any(
                field_type != "boolean" and not bool(value)
                for value, field_type in vals_types.values()
            )
            if has_non_boolean_false_value:
                continue
            vals = {key: val[0] for key, val in vals_types.items()}
            # Extract the "name" field (if present)
            name_field = next(
                (key for key in vals if key.endswith(".name") or key == "name"), 0
            )
            # Skip if "name" has the same value as another field
            if name_field:
                other_values = {
                    key: value for key, value in vals.items() if key != name_field
                }
                if vals[name_field] in other_values.values():
                    continue
            # Format pattern and vals
            # fmap = {"m2o_id.id": "f1", "name": "f2"}
            # fpattern "{m2o_id.id:>03} {name}" to "{f1:>03} {f2}"
            # fvals {"m2o_id.id": 1, "name": "test"} to {f1: 1, f2: "test"}
            def f_replace(match):
                full_placeholder = match.group(0)
                field_name = match.group(1)
                format_spec = match.group(2) or ""
                if field_name in fmap:
                    return f"{{{fmap[field_name]}{format_spec}}}"
                return full_placeholder

            fmap = {f: f"f{i}" for i, f in enumerate(vals.keys(), start=1)}
            fpattern = re.sub(r"\{([\w.]+)(:[^}]*)?\}", f_replace, pattern)
            fvals = {fkey: vals[key] for key, fkey in fmap.items()}
            record.display_name = fpattern.format(**fvals)
        return True

    def _get_display_name_field_paths(self):
        M = self.env["ir.model"]
        return M.search([("model", "=", self._name)])._get_display_name_field_paths()
