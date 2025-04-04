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
            "Example: '{id:>05} - {name}'\n"
            "Use python string format syntax.\n\n"
            "Conditions for displaying a record like the pattern:\n"
            "1. The field values are different and non-empty.\n"
            "2. No other module will _compute_display_name()."
        ),
    )

    @api.constrains("display_name_pattern")
    def _check_display_name_field_paths(self):
        def valid(field_path):
            try:
                fields = field_path.split('.')
                current_model = self.env[model.model]
                for field in fields:
                    has_id = hasattr(current_model, 'id')
                    fields = current_model._fields
                    field_def = current_model._fields.get(field)
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
            field_paths = model._get_display_name_field_paths()
            for field_path in field_paths:
                if not valid(field_path):
                    raise ValidationError(
                        f"_check_display_name_field_paths: "
                        f"field_path {field_path} is not valid."
                    )

    def _get_display_name_field_paths(self):
        regexp = r"\{([\w.]+)(?:[:!][^}]*)?\}"
        pattern = self._get_display_name_pattern()
        field_paths = [match.group(1) for match in re.finditer(regexp, pattern)]
        return tuple(field_paths)

    def _get_display_name_pattern(self):
        if not self:
            return ""
        if "display_name_pattern" in self._fields:
            self.ensure_one()
            # Do not prefetch fields (to install apps without errors).
            return self.with_context(prefetch_fields=False).display_name_pattern or ""
        else:
            return ""
