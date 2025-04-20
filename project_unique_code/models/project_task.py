from odoo import models

PROJECT_TASK_WRITABLE_FIELDS = {
    "unique_code",
}


class ProjectTask(models.Model):
    _inherit = "project.task"

    @property
    def SELF_WRITABLE_FIELDS(self):
        return super().SELF_WRITABLE_FIELDS | PROJECT_TASK_WRITABLE_FIELDS
