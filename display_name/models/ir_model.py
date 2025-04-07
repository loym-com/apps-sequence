# -*- coding: utf-8 -*-

import logging
import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    def _use_custom_display_name(self):
        name = "display_name.use_custom_display_name"
        param = self.env["ir.config_parameter"].sudo().get_param(name)
        self.use_custom_display_name = param == "True" if param else False

    use_custom_display_name = fields.Boolean(compute="_use_custom_display_name")

    display_name_pattern = fields.Char(
        string="Display Name",
        help=(
            "Example: '{parent_id.display_code}/{display_code} - {name}'\n"
            "Use python string format syntax.\n\n"
            "Conditions for displaying a record like the pattern:\n"
            "1. The field values are non-false (boolean field may be False)."
            "2. The name has a different value than the other fields.\n"
            "3. No other module will _compute_display_name()."
        ),
    )
    display_code_pattern = fields.Char(
        string="Display Code",
        help=(
            "Example: 'Y{create_date:%y}-{id:>03}'\n"
            "Use python string format syntax."
        ),
    )

    @api.constrains("display_name_pattern")
    def _check_display_name_field_paths(self):
        return self._check_display_field_paths("display_name_pattern")
    
    @api.constrains("display_code_pattern")
    def _check_display_code_field_paths(self):
        return self._check_display_field_paths("display_code_pattern")
    
    def _check_display_field_paths(self, field_name):
        def valid(field_path):
            try:
                field_names = field_path.split('.')
                current_model = self.env[model.model]
                for field_name in field_names:
                    has_id = hasattr(current_model, 'id')
                    fields = current_model._fields
                    field_def = current_model._fields.get(field_name)
                    if not field_def:
                        return False
                    if field_def.type in ('many2one', 'one2many', 'many2many'):
                        current_model = self.env[field_def.comodel_name]
                    else:
                        pass
                return True
            except Exception:
                return False

        for model in self:
            field_paths = model._get_display_field_paths(field_name)
            for field_path in field_paths:
                if not valid(field_path):
                    raise ValidationError(
                        f"_check_display_name_field_paths: "
                        f"field_path {field_path} is not valid."
                    )

    def set_missing_stored_display_code(self):
        self.ensure_one()
        Model = self.env[self.model].with_context(active_test=False)
        field = Model._fields["display_code"]
        if field.store and self.display_code_pattern:
            records = Model.search([("display_code", "=", False)])
            records._compute_display_code()
