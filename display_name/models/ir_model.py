# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

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
