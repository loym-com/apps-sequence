from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.constrains("unique_code", "name")
    def _set_alias_name_and_documents_folder_name(self):
        for record in self:
            # Set alias name
            record.alias_name = record.unique_code
            # Set documents folder name if it exists
            if record._fields.get("documents_folder_id") and record.documents_folder_id:
                record.documents_folder_id.name = record.display_name
