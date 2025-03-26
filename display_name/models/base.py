# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import re

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Base(models.AbstractModel):
    _inherit = "base"

    @staticmethod
    def _get_display_name_re():
        return r"%\((\w+)\)s"

    def _get_display_name_pattern(self):
        pattern = self.env["ir.model"].search_read(
            domain=[("model", "=", self._name)], fields=["display_name_pattern"]
        )[0].get("display_name_pattern")
        return pattern or ""

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

        reg_exp = self._get_display_name_re()
        pattern = self._get_display_name_pattern()
        for record in self:
            # Dynamically fetch field values based on the pattern
            try:
                field_values = {
                    field_name: getattr(record, field_name, "")
                    for field_name in record._get_display_name_fields()
                }
                # Condition for display_name
                if fields_are_filled_and_different(field_values):
                    record.display_name = pattern % field_values
            except KeyError as e:
                raise ValueError(
                    f"Field '{e.args[0]}' does not exist in model '{self._name}'."
                )

    # @staticmethod
    # def _extract_field_names(pattern):

    # @staticmethod
    # def _get_display_name_pattern_field_names(self):
    #     pattern = self._get_display_name_pattern()
    #     # Example: "%(sequence_code)s - %(name)s" -> ["sequence_code", "name"]
    #     return re.findall(r"%\((\w+)\)s", pattern)


    # @api.model
    # def name_search(self, name="", args=None, operator="ilike", limit=100):
    #     """Allow searching by sequence code by default."""
    #     result = super().name_search(name, args, operator, limit)
    #     # Do not add any domain when user just clicked on search widget
    #     if not (name == "" and operator == "ilike"):
    #         # We need additional search, as in super() method call expression
    #         # `AND` is used and there is no easy way to add `OR` in the final domain
    #         projects = self.search_fetch(
    #             [
    #                 ("sequence_code", operator, name),
    #                 "!",
    #                 ("display_name", operator, name),
    #             ],
    #             ["display_name"],
    #             limit=limit,
    #         ).mapped(lambda p: (p.id, p.display_name))
    #         result.extend(projects)
    #     return result

    # def name_search(self, name="", args=None, operator="ilike", limit=100):
    #     """
    #     Override name_search to search across all fields in the display_name_pattern.
    #     """
    #     result = super().name_search(name, args, operator, limit)

    #     args = args or []
    #     domain = args

    #     if name:
    #         # Extract fields from the display_name_pattern
    #         field_names = self._get_display_name_fields()
    #         search_domains = [
    #             (field_name, operator, name) for field_name in field_names if field_name in self._fields
    #         ]
    #         domain = ["|"] * (len(search_domains) - 1) + search_domains + args

    #     return self.search(domain, limit=limit).name_get()
    
    #     # normal search
    #     result.extend(super().name_search(name, domain, operator, limit))
    #     return result