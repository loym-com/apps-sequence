# Copyright 2025 Loym AS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_custom_display_name = fields.Boolean(
        string="Custom Display Names",
        config_parameter="display_name.use_custom_display_name",
        help=("Choose how to see records in a list, e.g. '{id:>05} - {name}'"),
    )
