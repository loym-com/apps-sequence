# -*- coding: utf-8 -*-

import logging
import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    display_name_pattern = fields.Char(
        string="Name Pattern",
        help=(
            "Example: '{parent_id.display_code}/{display_code} - {name}'\n"
            "Use python string format syntax.\n\n"
            "Conditions for displaying a record like the pattern:\n"
            "1. The field values are non-false (boolean field may be False)."
            "2. The name has a different value than the other fields.\n"
            "3. No other module will _compute_display_name()."
        ),
    )

    @api.constrains("display_name_pattern")
    def _check_display_name_field_paths(self):
        return self._check_display_field_paths("display_name_pattern")

    def _check_display_field_paths(self, field_name):
        for model in self:
            Model = self.env[model.model]
            field_paths = Model._get_display_field_paths(field_name, validate=False)
            if not Model._is_valid_display_field_paths(field_paths):
                raise ValidationError(
                    f"_check_display_name_field_paths: "
                    f"At least one field is not valid: {field_paths}"
                )
