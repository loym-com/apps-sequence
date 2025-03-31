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

        def get_nested_value(record, field_path):
            """
            Retrieve a nested value from the record using dot notation.
            """
            fields = field_path.split(".")
            value = record
            for field in fields:
                if value and hasattr(value, field):
                    value = getattr(value, field)
                else:
                    return None
            return value
        
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
            # Collect values for the field paths
            vals = {}
            for field_path in field_paths:
                value = get_nested_value(record, field_path)
                if value is not None:
                    vals[field_path] = value

            # Check if all fields have values
            if len(vals) == len(field_paths):
                # Extract the "name" field (if present)
                name_field = next(
                    (key for key in vals if key.endswith(".name") or key == "name"), 0
                )

                # Check if "name" is different from the other values
                if name_field:
                    other_values = {
                        key: value for key, value in vals.items() if key != name_field
                    }
                    if vals[name_field] not in other_values.values():
                            # Replace placeholders in the pattern with the actual values
                            record.display_name = re.sub(
                                r"\{([\w.]+)\}",
                                lambda match: str(vals[match.group(1)]),
                                pattern,
                            )
        return True

    def _get_display_name_field_paths(self):
        M = self.env["ir.model"]
        return M.search([("model", "=", self._name)])._get_display_name_field_paths()
