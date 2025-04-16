# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import api, fields, models
from odoo.tools.translate import _


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model_create_multi
    def create(self, vals_list):
        """Set sequence code for each record in vals_list."""
        vals_list = self.set_sequence_code(vals_list)
        return super().create(vals_list)
    
    def write(self, vals):
        """Set name = sequence code if removing name or no existing name"""

        if vals.get("name") or "name" not in self._fields:
            return super().write(vals)

        model = self.env["ir.model"].sudo().search([("model", "=", self._name)])
        if "sequence_code_field_id" not in model._fields:
            return super().write(vals)

        field = model.sequence_code_field_id
        if not field:
            return super().write(vals)

        for record in self:
            removing_name = bool("name" in vals and not vals.get("name"))
            existing_name = getattr(record, "name", False)
            if removing_name or not existing_name:
                sequence_code_field_name = field.name
                if sequence_code_field_name in vals:
                    vals["name"] = vals[sequence_code_field_name]
                else:
                    vals["name"] = getattr(record, sequence_code_field_name)
            super().write(vals)
        return True

    def set_sequence_code(self, vals_list=None):
        model = self.env["ir.model"].sudo().search([("model", "=", self._name)])
        # if "sequence_code_field_id" in model._fields and model.sequence_code_field_id:
        if model.sequence_code_field_id:
            FieldSudo = self.env["ir.model.fields"].sudo()
            field = FieldSudo.browse(model.sequence_code_field_id.id)
            if vals_list:
                # create
                for vals in vals_list:
                    if field.name not in vals:
                        # sequence code (sequence_choice needs vals)
                        vals[field.name] = self._get_next_sequence_code(vals)
                        # name (if empty)
                        if "name" in self._fields and not vals.get("name"):
                            vals["name"] = vals[field.name]
            else:
                # write
                for record in self:
                    if not getattr(record, field.name):
                        # sequence code (sequence_choice needs vals)
                        setattr(record, field.name, record._get_next_sequence_code())
                        # name (if empty)
                        if "name" in self._fields and not record.name:
                            record.name = getattr(record, field.name)
        return vals_list

    def _get_next_sequence_code(self, vals=None):
        "vals is needed by sequence_choice to read values of a record to be created."
        return self.env["ir.sequence"].next_by_code(self._name)
