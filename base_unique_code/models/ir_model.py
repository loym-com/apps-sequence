# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    def _compute_unique_code_field_exists(self):
        for record in self:
            field = self.env["ir.model.fields"].search(
                [
                    ("model_id", "=", record.id),
                    ("name", "=", "unique_code"),
                ],
            )
            record.unique_code_field_exists = bool(field)

    unique_code_field_exists = fields.Boolean(
        compute="_compute_unique_code_field_exists",
    )

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

    @api.constrains("unique_code_pattern")
    def _check_unique_code_field_paths(self):
        return self._check_display_field_paths("unique_code_pattern")

    # @api.onchange("unique_code_pattern")
    # def _onchange_unique_code_pattern(self):
    #     if self.unique_code_pattern:
    #         self.display_name_pattern = "{unique_code} {name}"
    #     else:
    #         self.display_name_pattern = False
