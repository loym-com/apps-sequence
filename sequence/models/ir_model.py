# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    def _use_custom_sequences(self):
        name = "sequence.use_custom_sequences"
        return bool(self.env["ir.config_parameter"].sudo().get_param(name) == "True")

    use_custom_sequences = fields.Boolean(compute="_use_custom_sequences")
    sequence_code_field_id = fields.Many2one(
        string="Store sequence in",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', field_id), ('ttype', 'in', ['char', 'text'])]",
        help="Select a field to store a sequence_code.\n"
            "If the field is readonly for the user, "
            "a new record will get a sequence code automatically.\n"
            "To get a sequence code for an existing record, "
            "click on Action - Set (Field Name, e.g. Sequence Code).\n\n"
            "This works because a Sequence and a Server Action are created.\n"
            "The Sequence has Code = (the technical name of the model).\n"
            "The Server Action has Model = (the name of the model).",
        ondelete="set null",
    )

    # Generic: manually set sequence_code_field_id
    # Module: set_sequence_code_field_id in res.config.settings and/or post_init_hook
    # Module uninstall: automatic ondelete set null
    def set_sequence_code_field_id(self, field_name=None):
        self.ensure_one()
        field_name = field_name or "sequence_code"
        field = self.env["ir.model.fields"].search(
            [("model_id", "=", self.id), ("name", "=", field_name)]
        )
        self.sequence_code_field_id = field.id

    @api.constrains("sequence_code_field_id")
    def set_sequence_and_action(self, vals={}):
        self.ensure_one()
        if self.sequence_code_field_id:
            self._set_sequence(self.model, vals)
            self._set_sequence_code_action()

    def _set_sequence(self, code, vals={}):
        Sequence = self.env["ir.sequence"]
        sequence = Sequence.search([("code", "=", code)])
        if not sequence:
            try:
                prefix = code.rsplit(".", 1)[1]
            except IndexError:
                prefix = code
            sequence = Sequence.create(
                {
                    "name": code,
                    "code": code,
                    "padding": 5,
                    "prefix": prefix + "-",
                }.update(vals)
            )
            _logger.info(f"Created sequence {sequence.name}")

    def _set_sequence_code_action(self):
        Action = self.env["ir.actions.server"]
        for model in self:
            if model.sequence_code_field_id:
                action = Action.search(
                    [
                        ("model_id", "=", model.id),
                        ("binding_model_id", "=", model.id),
                        ("usage", "=", "ir_actions_server"),
                        ("state", "=", "code"),
                        ("code", "=", "for rec in records:\n  rec.set_sequence_code()"),
                    ]
                )
                if not action:
                    name = f"Set {model.sequence_code_field_id.field_description}"
                    Action.create(
                        {
                            "model_id": model.id,
                            "binding_model_id": model.id,
                            "usage": "ir_actions_server",
                            "state": "code",
                            "name": name,
                            "code": "for rec in records:\n  rec.set_sequence_code()"
                        }
                    )
