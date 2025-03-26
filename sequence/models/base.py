# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model_create_multi
    def create(self, vals_list):
        """Set sequence code for each record in vals_list."""
        vals_list = self.sequence_code_set(vals_list)
        return super().create(vals_list)
    
    def sequence_code_get_model_info(self):
        domain = [("model", "=", self._name)]
        fields = ["sequence_code_field_id", "sequence_selection_field_id"]
        info = self.env["ir.model"].search_read(domain=domain, fields=fields)[0]
        return info

    def sequence_code_set(self, vals_list=None):
        """
        # if code_field:
        #   if vals_list:
        #       create
        #   else:
        #       write
        """
        info = self.sequence_code_get_model_info()

        def _get_sequence_code(rec_or_vals):
            if info.get("sequence_selection_field_id"):
                selection_field = self.env["ir.model.fields"].browse(info["sequence_selection_field_id"][0])
                if type(rec_or_vals) == dict:
                    value = rec_or_vals.get(selection_field.name)
                elif type(rec_or_vals) == type(self):
                    value = getattr(rec_or_vals, selection_field.name)
                    if selection_field.ttype == "many2one":
                        value = value.id
                else:
                    raise UserError(_("_get_sequence_code: Invalid type"))
                sequence_code = _get_custom_sequence_code(selection_field, value)
            else:
                sequence_code = self.env["ir.sequence"].next_by_code(self._name)
            return sequence_code

        def _get_custom_sequence_code(selection_field, value):
            value = str(value)
            code = f"{selection_field.model}.{selection_field.name}.{value}"
            return self.env["ir.sequence"].next_by_code(code)

        if info.get("sequence_code_field_id"):
            code_field = self.env["ir.model.fields"].browse(info["sequence_code_field_id"][0])
            if vals_list:
                for vals in vals_list:
                    if code_field.name not in vals:
                        vals[code_field.name] = _get_sequence_code(vals)
            else:
                for rec in self:
                    if not getattr(rec, code_field.name):
                        setattr(rec, code_field.name, _get_sequence_code(rec))
        return vals_list
