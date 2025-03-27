from odoo import models

PROJECT_TASK_WRITABLE_FIELDS = {
    "code",
}


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "sequence.mixin"]

    @property
    def SELF_WRITABLE_FIELDS(self):
        return super().SELF_WRITABLE_FIELDS | PROJECT_TASK_WRITABLE_FIELDS
