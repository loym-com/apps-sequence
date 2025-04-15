from odoo import api, fields, models


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    @api.ondelete(at_uninstall=True)
    def _check_model_display_patterns(self):
        for record in self:
            if record.name == "sequence_code":
                if "sequence_code" in record.model_id.display_code_pattern:
                    record.model_id.display_code_pattern = ""
                if "sequence_code" in record.model_id.display_name_pattern:
                    record.model_id.display_name_pattern = ""
