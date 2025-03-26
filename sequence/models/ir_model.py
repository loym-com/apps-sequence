# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    sequence_code_field_id = fields.Many2one(
        string="Store sequence in",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', field_id), ('ttype', 'in', ['char', 'text'])]",
        help="A new record will get a sequence code except if the user can set a value."
    )
    sequence_selection_field_id = fields.Many2one(
        string="A sequence for each",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', field_id), ('ttype', 'in', ['boolean', 'many2one', 'selection'])]",
    )

    @api.constrains("sequence_code_field_id", "sequence_selection_field_id")
    def _set_sequences(self):
        Sequence = self.env["ir.sequence"]

        def _set_sequence(code):
            seq = Sequence.search([("code", "=", code)])
            if not seq:
                try:
                    prefix = code.rsplit(".", 1)[1]
                except IndexError:
                    prefix = code
                seq = Sequence.create(
                    {
                        "name": code,
                        "code": code,
                        "padding": 5,
                        "prefix": prefix + "-",
                    }
                )
                _logger.info(f"Created sequence {seq.name}")

        for model in self:
            if not model.sequence_code_field_id:
                continue
            field = model.sequence_selection_field_id
            if field:
                if field.ttype == "boolean":
                    values = ["True", "False"]
                elif field.ttype == "many2one":
                    values = self.env[field.relation].search([]).mapped("id")
                    values = [str(value) for value in values]
                elif field.ttype == "selection":
                    values = field.selection_ids.mapped("value")
                else:
                    raise ValidationError(f"Unsupported field type {field.ttype}")

                for value in values:
                    code = f"{model.model}.{field.name}.{value}"
                    _set_sequence(code)
            else:
                code = f"{model.model}"
                _set_sequence(code)

    @api.constrains("sequence_code_field_id")
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
                        ("code", "=", "for rec in records:\n  rec.sequence_code_set()"),
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
                            "code": "for rec in records:\n  rec.sequence_code_set()"
                        }
                    )
