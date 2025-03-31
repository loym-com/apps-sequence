from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    project_project_display_name_pattern = fields.Char(
        string="Project Display Name",
        compute="_get_project_project_display_name_pattern",
        inverse="_set_project_project_display_name_pattern",
        default="{sequence_code} - {name}",
        help=(
            "Use sequence_code and name to include the sequence code "
            "and the name of the project in the display name."
        ),
    )
    project_task_display_name_pattern = fields.Char(
        string="Task Display Name",
        compute="_get_project_task_display_name_pattern",
        inverse="_set_project_task_display_name_pattern",
        default="[{sequence_code}] {name}",
        help=(
            "Use sequence_code and name to include the sequence code "
            "and the name of the task in the display name."
        ),
    )

    def _get_project_project_display_name_pattern(self):
        model = self.env["ir.model"].sudo().search([("model", "=", "project.project")])
        for record in self:
            record.project_project_display_name_pattern = model.display_name_pattern

    def _set_project_project_display_name_pattern(self):
        model = self.env["ir.model"].sudo().search([("model", "=", "project.project")])
        model.display_name_pattern = self.project_project_display_name_pattern

    def _get_project_task_display_name_pattern(self):
        model = self.env["ir.model"].sudo().search([("model", "=", "project.task")])
        for record in self:
            record.project_task_display_name_pattern = model.display_name_pattern

    def _set_project_task_display_name_pattern(self):
        model = self.env["ir.model"].sudo().search([("model", "=", "project.task")])
        model.display_name_pattern = self.project_task_display_name_pattern
