# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    def _use_custom_display_name(self):
        name = "display_name.use_custom_display_name"
        return bool(self.env["ir.config_parameter"].sudo().get_param(name) == "True")

    use_custom_display_name = fields.Boolean(compute="_use_custom_display_name")

    display_name_pattern = fields.Char(
        string="Display Name",
        help=(
            "Example: %(id)s - %(name)s \n"
            "The pattern will be used on a record "
            "if the values are different and non-empty."
        ),
    )

    def write(self, vals):
        super().write(vals)
        if "display_name_pattern" in vals:
            # _get_display_name_pattern() reads directly from the database
            self.env.cr.flush()

    # Use in res.config.settings and/or post_init_hook
    def set_display_name_pattern(
            self,
            display_name_pattern="%(sequence_code)s - %(name)s",
        ):
        self.ensure_one()
        self.display_name_pattern = display_name_pattern
