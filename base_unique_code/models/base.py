# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import psycopg2

from odoo import api, fields, models
from odoo.tools.translate import _

from odoo.addons.base_display_name.tools import get_value, is_none, set_value


class Base(models.AbstractModel):
    _inherit = "base"
    _sql_constraints = [
        (
            "unique_code",
            "UNIQUE(unique_code)",
            "unique_code must be unique!",
        ),
    ]

    unique_code = fields.Char(copy=False, index=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Set unique_code and name, if unique_code is not set."""
        vals_list_ok = [vals for vals in vals_list if "unique_code" in vals]
        vals_list_todo = [vals for vals in vals_list if "unique_code" not in vals]
        # Create first, so we can use the record "id" etc. in the pattern
        records_ok = super().create(vals_list_ok)
        records_todo = super().create(vals_list_todo)
        records_todo.set_unique_code_and_name()
        return records_ok | records_todo

    def write(self, vals):
        super().write(vals)
        self._set_name_if_empty()

    def set_unique_code_and_name(self, vals_list=None):
        vals_list = self._set_unique_code(vals_list)
        vals_list = self._set_name_if_empty(vals_list)
        return vals_list

    def _set_unique_code(self, vals_list=None):
        return self._set_field_from_pattern(
            "unique_code", "unique_code_pattern", vals_list
        )
    
    def _set_name_if_empty(self, vals_list=None):
        """Set name = unique_code if removing name or no existing name

        Checking if the record has a name may affect the performance..."""

        # Relevant for uninstalling the module
        context = self.env.context
        if "prefetch_fields" in context and not context.get("prefetch_fields"):
            return vals_list

        if "name" not in self._fields:
            return vals_list

        model = self._get_ir_model()
        pattern = model.unique_code_pattern
        if not pattern:
            return vals_list

        # Handle both create and write
        for item in vals_list or self:
            if get_value(item, "unique_code") and not get_value(item, "name"):
                set_value(item, "name", item["unique_code"])
        return vals_list

    # Override methods in base_display_name, to handle __sequence__.

    def _get_display_value(self, item, field_path):
        """Use sequence if:
        1) field_path is "__sequence__"
        2) ir.model has unique_code_sequence_id
        """
        if field_path == "__sequence__" and is_none(item, "unique_code"):
            sequence = self._get_ir_model(prefetch_fields=False).unique_code_sequence_id
            if sequence:
                return (sequence.next_by_id(), "char")
        return super()._get_display_value(item, field_path)

    def _is_valid_display_field_paths(self, field_paths):
        """Do not check __sequence__."""
        field_paths = [item for item in field_paths if item != "__sequence__"]
        return super()._is_valid_display_field_paths(field_paths)
