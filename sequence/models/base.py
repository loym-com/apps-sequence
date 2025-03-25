# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model_create_multi
    def create(self, vals_list):
        """Set sequence code for each record in vals_list."""
        # sequence_code_get_model_info
        # model = self.env["ir.model"].search([("model", "=", self._name)])
        vals_list = self.sequence_code_set(vals_list)
        res = super().create(vals_list)
        # res._sync_analytic_account_name()
        # res.sequence_code_run_extra_action(model)
        return res
        # model = self.env["ir.model"].search([("model", "=", self._name)])
        # selection_field = model.sequence_selection_field_id
        # code_field = model.sequence_code_field_id

        # if code_field:
        #     for vals in vals_list:
        #         if selection_field:
        #             value = vals.get(selection_field.name)
        #             sequence_code = self._get_custom_sequence_code(selection_field, value)
        #         else:
        #             sequence_code = self.env["ir.sequence"].next_by_code(self._name)
        #         vals[code_field.name] = sequence_code


    # def set_sequence_code(self):
    #     model = self.env["ir.model"].search([("model", "=", self._name)])
    #     selection_field = model.sequence_selection_field_id
    #     code_field = model.sequence_code_field_id

    #     for rec in self:
    #         if selection_field:
    #             value = getattr(rec, selection_field.name)
    #             sequence_code = self._get_custom_sequence_code(selection_field, value)
    #         else:
    #             sequence_code = self.env["ir.sequence"].next_by_code(self._name)
    #         setattr(rec, code_field.name, sequence_code)

    # def _get_custom_sequence_code(self, selection_field, value):
    #     value = str(value)
    #     code = f"{selection_field.model}.{selection_field.name}.{value}"
    #     return self.env["ir.sequence"].next_by_code(code)

    # def write(self, vals):
    #     res = super().write(dict(vals, name=name))
    #     self.sequence_code_run_extra_action
    #     """Sync name and analytic account name when name is changed."""
    #     # If name isn't changing, nothing special to do
    #     if "name" not in vals and "sequence_name" not in vals:
    #         return super().write(vals)
    #     # When changing name, we need to update the analytic account name too
    #     for one in self:
    #         sequence_code = vals.get("sequence_code", one.sequence_code)
    #         name = vals.get("name") or sequence_code
            
    #     self._sync_analytic_account_name()
    #     return True
    
    def sequence_code_get_model_info(self):
        domain = [("model", "=", self._name)]
        fields = ["sequence_code_field_id", "sequence_selection_field_id"]
        info = self.env["ir.model"].search_read(domain=domain, fields=fields)[0]
        return info

    def sequence_code_set(self, vals_list=None):
        """
        # If code_field:
        #   If vals_list:
        #       create ->
        #           - sequence_code_set
        #           - super(create)
        #           - sequence_code_run_extra_action
        #   Else:
        #       sequence_code_set -> write -> sequence_code_run_extra_action"
        """

        # model = model or self.env["ir.model"].search([("model", "=", self._name)])
        # selection_field = model.sequence_selection_field_id
        # code_field = model.sequence_code_field_id
        info = self.sequence_code_get_model_info()

        def _get_sequence_code(rec_or_vals):
            if info.get("sequence_selection_field_id"):
                selection_field = self.env["ir.model.fields"].browse(info["sequence_selection_field_id"])
                if type(rec_or_vals) == dict:
                    value = rec_or_vals.get(selection_field.name)
                elif type(rec_or_vals) == type(self):
                    value = getattr(rec_or_vals, selection_field.name)
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
            code_field = self.env["ir.model.fields"].browse(info["sequence_code_field_id"])
            if vals_list:
                for vals in vals_list:
                    if code_field.name not in vals:
                        vals[code_field.name] = _get_sequence_code(vals)
                return vals_list
            else:
                for rec in self:
                    setattr(rec, code_field.name, _get_sequence_code(rec))

    # def sequence_code_run_extra_action(self, model):
    #     domain = [("model", "=", self._name)]
    #     fields = ["sequence_code_extra_action_id"]
    #     extra_action = self.env["ir.model"].search_read(domain=domain, fields=fields)
    #     if extra_action:
    #         action = extra_action[0].get("sequence_code_extra_action_id")
    #         action.run()
