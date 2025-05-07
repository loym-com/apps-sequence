from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    internal_external = fields.Selection(
        string="Pi Pe",
        selection=[("internal", "Internal"), ("external", "External")]
    )

    @api.constrains("internal_external")
    def _onchange_internal_external(self):
        if self.unique_code:
            prefix = self.unique_code[:2] if self.unique_code[:2] in ("Pi", "Pe") else None
            if prefix:
                if self.internal_external == "internal":
                    self.unique_code = "Pi" + self.unique_code[2:]
                elif self.internal_external == "external":
                    self.unique_code = "Pe" + self.unique_code[2:]
            else:
                if self.internal_external == "internal":
                    self.unique_code = "Pi" + self.unique_code
                elif self.internal_external == "external":
                    self.unique_code = "Pe" + self.unique_code

    @api.constrains("unique_code", "name")
    def _constrains_unique_code(self):
        for record in self:
            record.alias_name = record.unique_code
            if record._fields.get("documents_folder_id") and record.documents_folder_id:
                record.documents_folder_id.name = record.display_name
