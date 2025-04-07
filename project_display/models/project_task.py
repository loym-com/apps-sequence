from odoo import api, models, fields


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "display.mixin"]
