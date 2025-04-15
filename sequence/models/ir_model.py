# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    def _use_custom_sequences(self):
        name = "sequence.use_custom_sequences"
        param = self.env["ir.config_parameter"].sudo().get_param(name)
        self.use_custom_sequences = param == "True" if param else False

    use_custom_sequences = fields.Boolean(compute="_use_custom_sequences")
    sequence_code_field_id = fields.Many2one(
        string="Sequence Code Field",
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
    )

    # Use in res.config.settings and/or post_init_hook.
    def set_sequence(self, field_name=None, sequence_values={}):
        self.ensure_one()
        # Set the sequence first, to apply custom values.
        self._create_missing_sequence(code=self.model, values=sequence_values)
        # Set the field.
        field = self.env["ir.model.fields"].search(
            [("model_id", "=", self.id), ("name", "=", field_name)]
        )
        self.sequence_code_field_id = field.id

    @api.constrains("sequence_code_field_id")
    def check_sequence_code_field_id(self):
        self.ensure_one()
        field = self.sequence_code_field_id
        if field:
            if field.ttype not in ("char", "text"):
                func_name = "check_sequence_code_field_id"
                raise ValidationError(
                    f"{func_name}: field {field.name} type should be char or text."
                )
            self._create_missing_sequence(code=self.model)
            self._create_missing_sequence_code_action()

    def _create_missing_sequence(self, code, values={}):
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
                } | values
            )
            _logger.info(f"Created sequence {sequence.name}")

    def _create_missing_sequence_code_action(self):
        if self.sequence_code_field_id:
            search_domain = [
                ("model_id", "=", self.id),
                ("binding_model_id", "=", self.id),
                ("usage", "=", "ir_actions_server"),
                ("state", "=", "code"),
                ("code", "=", "for rec in records:\n  rec.set_sequence_code()"),
            ]
            Action = self.env["ir.actions.server"]
            action = Action.search(search_domain)
            if not action:
                search_dict = {key: value for key, equal, value in search_domain}
                name = f"Set {self.sequence_code_field_id.field_description}"
                Action.create(search_dict | {"name": name})

    def _delete_patterns_with_sequence_code(self, model_names):
        models = self.search([("model", "in", model_names)])
        for model in models:
            if "sequence_code" in model.display_code_pattern:
                model.display_code_pattern = ""
            if "sequence_code" in model.display_name_pattern:
                model.display_name_pattern = ""
        models.flush()
