from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    project_display_name_pattern = fields.Char(
        # config_parameter="project_sequence.display_name_pattern",
        compute="_get_project_display_name_pattern",
        inverse="_set_project_display_name_pattern",
        default="%(sequence_code)s - %(name)s",
        help=(
            "Use %(sequence_code)s and %(name)s to include the sequence code "
            "and the name of the project in the display name."
        ),
    )

    def _get_project_display_name_pattern(self):
        model = self.env["ir.model"].search([("model", "=", "project.project")])
        for record in self:
            record.display_name_pattern = model.display_name_pattern

    def _set_project_display_name_pattern(self):
        model = self.env["ir.model"].search([("model", "=", "project.project")])
        model.display_name_pattern = self.display_name_pattern
