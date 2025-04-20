from odoo import api, fields, models
 
 
class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    @api.ondelete(at_uninstall=True)
    def _delete_patterns_with_unique_code(self):
        for record in self:
            if record.name == "unique_code":
                # if "unique_code" in record.model_id.unique_code_pattern:
                #     record.model_id.display_code_pattern = ""
                if "unique_code" in record.model_id.display_name_pattern:
                    record.model_id.display_name_pattern = ""
