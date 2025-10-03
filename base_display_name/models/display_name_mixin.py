import logging
import psycopg2
import re

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval
from odoo.tools.translate import _

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

    def _set_field_from_pattern_name(self, display_fname, pattern_name, source="ir.model"):
        """
        Set a field (e.g. "display_name" or "unique_code") based on a pattern.
        display_fname: The name of the display field to compute.
        pattern_name: The name of the ir.model field or ir.config_parameter key with the pattern.
        source: "ir.model" or "ir.config_parameter"
        """
        pattern = self._get_display_pattern(pattern_name, source=source)

        for record in self:
            # Skip if value exists in stored field
            if self._fields[display_fname].store and getattr(record, display_fname):
                continue
            # Set value
            value = record._get_value_from_pattern(pattern)
            if value:
                setattr(record, display_fname, value)

    def _get_value_from_pattern(self, pattern):
        if pattern:
            value = safe_eval(f"f{repr(pattern)}", {"r": self})
            if value:
                return value

    def _get_display_field_paths(self, pattern_name, validate=True):
        pattern = self._get_display_pattern(pattern_name)
        return self._get_display_field_paths_from_string(pattern, validate)

    def _get_display_field_paths_from_string(self, fields_input, validate=True):
        """fields_input: Either a pattern string with placeholders,
        e.g. "{r.field1} {r.field2}", or a comma-separated string, e.g. "field1, field2".
        return: tuple of field paths, e.g. ('field1', 'field2')
        """
        if "{" in fields_input and "}" in fields_input:
            # Treat as pattern string with placeholders
            # Regex from your pattern function: {field[:!format]}
            field_paths = extract_r_paths_from_template(fields_input)
            # regexp = r"r\.([a-zA-Z_][a-zA-Z0-9_\.]*)"
            # regexp = r"\{([\w.]+)(?:[:!][^}]*)?\}"
            # field_paths = [m.group(1) for m in re.finditer(regexp, fields_input)]
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
        if fields and fields[0] == "r":
            fields = fields[1:]
        model = self
        value = item
        for field in fields:
            if field in model._fields:
                value_type = model._fields.get(field).type
                value = getattr(value, field)
                model = value
            else:
                return (None, None)
        return (value, value_type)

def extract_r_paths_from_template(template):
    """
    Extract all attribute paths starting with `r.` from a template string.
    
    Handles formatting and simple conditionals in f-string style.
    Returns a set of attribute paths without the leading 'r.'.
    """
    # 1️⃣ Match everything inside braces {}
    brace_pattern = r"\{([^{}]+)\}"  # matches { … } contents
    matches = re.findall(brace_pattern, template)
    
    # 2️⃣ For each match, extract r.something paths
    r_path_pattern = r"r\.([a-zA-Z_][a-zA-Z0-9_\.]*)"
    paths = set()
    for expr in matches:
        found = re.findall(r_path_pattern, expr)
        paths.update(found)
    
    return paths
