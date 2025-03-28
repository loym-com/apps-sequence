# Copyright 2025 Loym AS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_custom_sequences = fields.Boolean(
        string="Use Custom Sequences",
        config_parameter="sequence.use_custom_sequences",
        help=(
            "Each record may have a sequence code. "
            "Each model may have a field to determine "
            "how to generate the sequence code."
        ),
    )
