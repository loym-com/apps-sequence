from odoo import api, models, fields


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "display.mixin"]
