from odoo import models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def module_uninstall(self):
        for module in self:
            if module.name == "sequence_project":
                self.env["ir.model"].search(
                    [("model", "in", ("project.project", "project.task"))]
                )._delete_patterns_with_sequence_code()

        return super(IrModuleModule, self).module_uninstall()
