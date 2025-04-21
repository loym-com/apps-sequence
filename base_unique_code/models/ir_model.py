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

    @api.constrains("unique_code_pattern")
    def _set_action_compute_unique_code(self):
        """If pattern, create action. If no pattern, delete action."""
        for record in self:
            search_domain = [
                ("model_id", "=", record.id),
                ("binding_model_id", "=", record.id),
                ("usage", "=", "ir_actions_server"),
                ("state", "=", "code"),
                ("code", "=", "records.set_unique_code_and_name()"),
            ]
            Action = self.env["ir.actions.server"]
            action = Action.search(search_domain)
            if record.unique_code_pattern and not action:
                search_dict = {key: value for key, equal, value in search_domain}
                name = "Set unique code"
                Action.create(search_dict | {"name": name})
            elif action and not record.unique_code_pattern:
                action.unlink()
