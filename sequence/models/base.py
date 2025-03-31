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
        """If no name, then name = sequence code"""
        if vals.get("name") or "name" not in self._fields:
            return super().write(vals)

        model = self.env["ir.model"].sudo().search([("model", "=", self._name)])
        field = model.sequence_code_field_id
        if not field:
            return super().write(vals)

        for record in self:
            if not record.name:
                if field.name in vals:
                    vals["name"] = vals[field.name]
                else:
                    vals["name"] = getattr(record, field.name)
            super().write(vals)
        return True

    def set_sequence_code(self, vals_list=None):
        model = self.env["ir.model"].sudo().search([("model", "=", self._name)])
        # if "sequence_code_field_id" in model._fields and model.sequence_code_field_id:
        if model.sequence_code_field_id:
            field = self.env["ir.model.fields"].browse(model.sequence_code_field_id.id)
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
