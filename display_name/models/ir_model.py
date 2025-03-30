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
            "Example: '{id:05} - {name}'\n"
            "Use python string format syntax.\n\n"
            "Conditions for displaying a record like the pattern:\n"
            "1. The field values are different and non-empty.\n"
            "2. No other module will _compute_display_name()."
        ),
    )

    @api.constrains("display_name_pattern")
    def _check_display_name_field_names(self):
        for model in self:
            field_names = model._get_display_name_field_names()
            fields = self.env["ir.model.fields"].search(
                [("model", "=", self.model), ("name", "in", field_names)]
            )
            if not len(field_names) == len(fields):
                msg = f"_check_display_name_field_names: not all exist: {field_names!s}"
                raise ValidationError(msg)

    def _get_display_name_field_names(self):
        regexp = r"\{(\w+)(?:[:!][^}]*)?\}"
        pattern = self._get_display_name_pattern()
        field_names = [match.group(1) for match in re.finditer(regexp, pattern)]
        return tuple(field_names)

    def _get_display_name_pattern(self):
        if not self:
            return ""
        if "display_name_pattern" in self._fields:
            self.ensure_one()
            # Do not prefetch fields (to install apps without errors).
            return self.with_context(prefetch_fields=False).display_name_pattern or ""
        else:
            return ""
