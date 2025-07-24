from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.base_display_name.tools import get_value, is_none, set_value


class UniqueCodeMixin(models.AbstractModel):
    _inherit = "unique.code.mixin"

    def _set_sequence_code(self, vals_list=None):
        """Set sequence_code based on the ir.model's sequence_choice_field_id."""
        choice_field = self._get_ir_model(prefetch_fields=False).sequence_choice_field_id
        if choice_field:
            for item in vals_list or self:
                if is_none(item, "sequence_code"):
                    choice_value = item[choice_field.name]
                    if choice_field.ttype == "many2one":
                        choice_value = choice_value.id
                    choice_value = str(choice_value)
                    code = f"{choice_field.model}.{choice_field.name}.{choice_value}"
                    sequence_code = self.env["ir.sequence"].next_by_code(code)
                    if sequence_code:
                        set_value(item, "sequence_code", sequence_code)
                    else:
                        raise UserError(
                             "No sequence found for code:\n"
                            f"{code}\n\n"
                             "Please create a sequence for this code.\n\n"
                            f"Or go to Settings - Technical - Database Structure - Models - {choice_field.model}.\n"
                             "CHOOSE SEQUENCE BY:\n"
                             "- Remember the current setting.\n"
                             "- Set the field to blank and save.\n"
                             "- Set the field to the remembered value and save.\n"
                             "Then go to Sequences and configure the new sequence(s)."
                        )
            return vals_list
        else:
            return super()._set_sequence_code(vals_list)
