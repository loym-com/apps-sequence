import logging
import psycopg2
import re

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.translate import _

from odoo.addons.base_display_name.tools import get_value, is_none, set_value, get_indexed_pattern

_logger = logging.getLogger(__name__)


class DisplayNameMixin(models.AbstractModel):
    _name = "display.name.mixin"
    _description = "display.name.mixin"

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
        super()._compute_display_name()
        self._set_field_from_pattern_name("display_name", "display_name_pattern")

    # low-level

    def _set_field_from_pattern_name(self, display_fname, pattern_name, vals_list=None, source="ir.model"):
        """
        Set a field (e.g. "display_name" or "unique_code") based on a pattern.
        display_fname: The name of the display field to compute.
        pattern_name: The name of the ir.model field or ir.config_parameter key with the pattern.
        vals_list: Records to create. Loop through vals_list or self.
        source: "ir.model" or "ir.config_parameter"
        """
        pattern = self._get_display_pattern(pattern_name, source=source)
        field_paths = self._get_display_field_paths_from_string(pattern)
        if not field_paths:
            return vals_list
        indexed_pattern = get_indexed_pattern(pattern, field_paths)

        # Handle both create and write
        for item in vals_list or self:
            # Skip if value exists in stored field
            if self._fields[display_fname].store and not is_none(item, display_fname):
                continue
            # Set value
            value = self._get_value_from_indexed_pattern(item, field_paths, indexed_pattern)
            if value:
                set_value(item, display_fname, value)
        return vals_list

    def _get_value_from_indexed_pattern(self, item, field_paths, indexed_pattern):
        """
        Set a field (e.g. "display_name" or "unique_code") based on an pattern.
        pattern: E.g. "{field1} {field2}"
        field_paths: E.g. ('field1', 'field2')
        indexed_pattern: E.g. "{0} {1}"
        """

        # Collect values, and check for false values
        vals = {}
        name_vals = {}
        false_value = False
        for i, field_path in enumerate(field_paths):
            value, value_type = self._get_display_value(item, field_path)
            if not value and value_type != "boolean":
                false_value = True
                break
            vals[i] = value
            if field_path.endswith(".name") or field_path == "name":
                name_vals[i] = value
        # Check if "name" values are unique, or if another field has the same value
        name_not_unique = False
        for i, value in name_vals.items():
            if value in {v for k, v in vals.items() if k != i}:
                name_not_unique = True
                break
        # Conditions
        if false_value or name_not_unique:
            return
        # Set the display field value
        return indexed_pattern.format(*vals.values())

    def _get_display_field_paths(self, pattern_name, validate=True):
        pattern = self._get_display_pattern(pattern_name)
        return self._get_display_field_paths_from_string(pattern, validate)

    def _get_display_field_paths_from_string(self, fields_input, validate=True):
        """fields_input: Either a pattern string with placeholders,
        e.g. "{field1} {field2}", or a comma-separated string, e.g. "field1, field2".
        return: tuple of field paths, e.g. ('field1', 'field2')
        """
        if "{" in fields_input and "}" in fields_input:
            # Treat as pattern string with placeholders
            # Regex from your pattern function: {field[:!format]}
            regexp = r"\{([\w.]+)(?:[:!][^}]*)?\}"
            field_paths = [m.group(1) for m in re.finditer(regexp, fields_input)]
        else:
            # Treat as comma-separated list
            field_paths = [part.strip() for part in fields_input.split(",") if part.strip()]

        if not validate:
            return tuple(field_paths)
        elif self._is_valid_display_field_paths(field_paths):
            return tuple(field_paths)
        else:
            return ()

    def _is_valid_display_field_paths(self, field_paths):
        tuples = [
            self._get_display_value(self.browse(), field_path)
            for field_path in field_paths
        ]
        if (None, None) in tuples:
            return False
        else:
            return True

    def _get_display_pattern(self, pattern_name, source="ir.model"):
        """pattern_name: The name of the ir.model field or ir.config_parameter key
        with the pattern."""

        # To install apps without errors:
        # - Do not prefetch fields.
        if source == "ir.model":
            model = self._get_ir_model(prefetch_fields=False)
            return getattr(model, pattern_name) or ""
        elif source == "ir.config_parameter":
            param = self.env["ir.config_parameter"].sudo().get_param(pattern_name)
            return param or ""

    def _get_ir_model(self, prefetch_fields=True):
        IrModel = self.env["ir.model"].sudo()
        IrModel = IrModel.with_context(prefetch_fields=prefetch_fields)
        domain = [("model", "=", self._name)]
        # To install apps without errors:
        # - Order by a field which always exists.
        return IrModel.search([("model", "=", self._name)], order="id")

    def _get_display_value(self, item, field_path):
        """
        item: 0-1 records or vals to create a record
        field_path may use dot notation, e.g. related_id.field"
        return: (value, value_type)
        """
        fields = field_path.split(".")
        model = self
        value = item
        for field in fields:
            if field in model._fields:
                value_type = model._fields.get(field).type
                value = get_value(value, field)
                model = value
            else:
                return (None, None)
        return (value, value_type)
