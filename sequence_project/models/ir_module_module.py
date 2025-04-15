from odoo import models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def module_uninstall(self):
        # Delete patterns with sequence_code
        for module in self:
            if module.name == "sequence_project":
                self.env["ir.model"]._delete_patterns_with_sequence_code(
                    model_names=("project.project", "project.task")
                )
        return super().module_uninstall()
