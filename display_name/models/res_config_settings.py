# Copyright 2025 Loym AS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_custom_display_name = fields.Boolean(
        string="Use Custom Display Name",
        config_parameter="display_name.use_custom_display_name",
        help=(
            "Each record may have a sequence code. "
            "Each model may have a custom display name, "
            "e.g. '%(id)s - %(name)s'"
        ),
    )
