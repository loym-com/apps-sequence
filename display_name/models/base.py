import re

from odoo import api, models
from odoo.osv import expression
from odoo.tools.translate import _

class Base(models.AbstractModel):
    _inherit = "base"

    @staticmethod
    def _get_display_name_re():
        return r"%\((\w+)\)s"

    def _get_display_name_pattern(self):
        try:
            pattern = self.env["ir.model"].search_read(
                domain=[("model", "=", self._name)], fields=["display_name_pattern"]
            )[0].get("display_name_pattern")
            return pattern or ""
        except IndexError:
            # This error occurs when installing a new addon.
            return ""

    def _get_display_name_fields(self):
        fields = re.findall(
            self._get_display_name_re(), self._get_display_name_pattern()
        )
        return tuple(fields)
    
    @api.depends(lambda self: self._get_display_name_fields())
    def _compute_display_name(self):
        res = super()._compute_display_name()

        def fields_are_filled_and_different(field_values):
            # Check if there are any fields
            if not field_values:
                return False
            
            # Check if all fields have a non-empty value
            if not all(field_values.values()):
                return False

            # Check if all values are different
            values = list(field_values.values())
            if len(values) != len(set(values)):
                return False

            return True

        pattern = self._get_display_name_pattern()
        field_names = self._get_display_name_fields()
        for record in self:
            # Dynamically fetch field values based on the pattern
            try:
                field_values = {
                    field_name: getattr(record, field_name, "")
                    for field_name in field_names
                }
                # Condition for display_name
                if fields_are_filled_and_different(field_values):
                    record.display_name = pattern % field_values
            except KeyError as e:
                raise ValueError(
                    f"Field '{e.args[0]}' does not exist in model '{self._name}'."
                )

    @api.model
    def _search_display_name(self, operator, value):
        search_fnames = self._get_display_name_fields()
        if not search_fnames:
            return super()._search_display_name(operator, value)

        # Copied from ORM models.py
        if operator.endswith('like') and not value and '=' not in operator:
            # optimize out the default criterion of ``like ''`` that matches everything
            # return all when operator is positive
            return expression.FALSE_DOMAIN if operator in expression.NEGATIVE_TERM_OPERATORS else expression.TRUE_DOMAIN
        aggregator = expression.AND if operator in expression.NEGATIVE_TERM_OPERATORS else expression.OR
        return aggregator([[(field_name, operator, value)] for field_name in search_fnames])
