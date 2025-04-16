import logging
import psycopg2
import re

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class Base(models.AbstractModel):
    _inherit = "base"

    # display_name

    @api.model
    def _search_display_name(self, operator, value):
        search_fnames = self._get_display_field_paths("display_name_pattern")
        if not search_fnames:
            return super()._search_display_name(operator, value)

        # Copied from ORM models.py
        if operator.endswith('like') and not value and '=' not in operator:
            # optimize out the default criterion of ``like ''`` that matches everything
            # return all when operator is positive
            return expression.FALSE_DOMAIN if operator in expression.NEGATIVE_TERM_OPERATORS else expression.TRUE_DOMAIN
        aggregator = expression.AND if operator in expression.NEGATIVE_TERM_OPERATORS else expression.OR
        return aggregator([[(field_name, operator, value)] for field_name in search_fnames])
    
    @api.depends(lambda self: self._get_display_field_paths("display_name_pattern"))
    def _compute_display_name(self):
        res = super()._compute_display_name()
        return self._compute_display_field("display_name", "display_name_pattern", res)
    
    # display_code

    display_code = fields.Char(
        compute="_compute_display_code",
        inverse="_inverse_display_code",
        store=False, # in base; set True for a specific model in a custom module
        copy=False,
    )

    @api.depends(lambda self: self._get_display_field_paths("display_code_pattern"))
    def _compute_display_code(self):
        return self._compute_display_field("display_code", "display_code_pattern")
    
    def _inverse_display_code(self):
        for record in self:
            record.display_code = record.display_code

    # low-level

    def _compute_display_field(self, display_fname, pattern_fname, res=True):
        """
        Compute a field (e.g. display_name or display_code) based on a pattern.
        display_fname: The name of the display field to compute.
        pattern_fname: The name of the ir.model field with the pattern.
        """

        def get_indexed_pattern(pattern, field_paths):
            def replace_path_with_index(match):
                full_placeholder = match.group(0)
                field_path = match.group(1)
                format_spec = match.group(2) or ""
                if field_path in field_paths:
                    return f"{{{field_paths.index(field_path)}{format_spec}}}"
                else:
                    return full_placeholder
            return re.sub(r"\{([\w.]+)(:[^}]*)?\}", replace_path_with_index, pattern)

        pattern = self._get_display_pattern(pattern_fname)
        field_paths = self._get_display_field_paths_from_pattern(pattern)
        if not field_paths:
            return res
        indexed_pattern = get_indexed_pattern(pattern, field_paths)

        for record in self:
            # Skip if value exists in stored field
            if record._fields[display_fname].store and getattr(record, display_fname):
                continue
            # Collect values, and check for false values
            vals = {}
            name_vals = {}
            false_value = False
            for i, field_path in enumerate(field_paths):
                value, value_type = record._get_display_value_and_type(field_path)
                if not value and value_type != "boolean":
                    false_value = True
                    break
                vals[i] = value
                if field_path.endswith(".name") or field_path == "name":
                    name_vals[i] = value
            # Check if "name" values are unique
            name_not_unique = False
            for i, value in name_vals.items():
                if value in {v for k, v in vals.items() if k != i}:
                    name_not_unique = True
                    break
            # Conditions
            if false_value or name_not_unique:
                continue
            # Set the display field value
            setattr(record, display_fname, indexed_pattern.format(*vals.values()))
        return res

    def _get_display_field_paths(self, pattern_fname, validate=True):
        pattern = self._get_display_pattern(pattern_fname)
        return self._get_display_field_paths_from_pattern(pattern, validate)

    def _get_display_field_paths_from_pattern(self, pattern, validate=True):
        regexp = r"\{([\w.]+)(?:[:!][^}]*)?\}"
        field_paths = [match.group(1) for match in re.finditer(regexp, pattern)]
        if not validate:
            return tuple(field_paths)
        elif self._is_valid_display_field_paths(field_paths):
            return tuple(field_paths)
        else:
            return ()

    def _is_valid_display_field_paths(self, field_paths):
        tuples = [self.browse()._get_display_value_and_type(p) for p in field_paths]
        if (None, None) in tuples:
            return False
        else:
            return True

    def _get_display_pattern(self, pattern_fname):
        """pattern_fname: The name of the ir.model field with the pattern."""
        # if self._name == "ir.model":
        #     return ""

        # To install apps without errors:
        # - Do not prefetch fields.
        # - Order by a field which always exists.
        IrModel = self.env["ir.model"].sudo().with_context(prefetch_fields=False)
        model = IrModel.search([("model", "=", self._name)], order="id")
        model_pattern = model._get_display_value_and_type(pattern_fname)
        if model_pattern and model_pattern[0]:
            return model_pattern[0] or ""
        else:
            return ""

    def _get_display_value_and_type(self, field_path):
        # self: 0-1 records
        # field_path may use dot notation, e.g. related_id.field"
        fields = field_path.split(".")
        value = self
        for field in fields:
            if field in value._fields:
                field_type = value._fields.get(field).type
                value = getattr(value, field)
            else:
                return (None, None)
        return (value, field_type)
