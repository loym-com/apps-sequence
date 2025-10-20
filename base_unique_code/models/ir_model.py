# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    unique_code_pattern = fields.Char(
        string="Code Pattern",
        help=(
            "Example: 'Y{create_date:%y}-{id:>03}'\n"
            "Use python string format syntax."
        ),
    )
    unique_code_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Code Sequence",
    )
