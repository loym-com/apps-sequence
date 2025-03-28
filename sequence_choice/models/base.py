from odoo import api, fields, models


class Base(models.AbstractModel):
    _inherit = "base"

    def _get_sequence_code(self, vals=None):
        "vals is needed by sequence_choice to read values of a record to be created."
        model = self.env["ir.model"].search([("model", "=", self._name)])
        choice_field_id = model.sequence_choice_field_id
        if choice_field_id:
            choice_field = self.env["ir.model.fields"].browse(choice_field_id.id)
            if vals:
                choice_value = vals.get(choice_field.name)
            else:
                self.ensure_one()
                choice_value = getattr(self, choice_field.name)
                # if choice_field.ttype == "many2one":
                #     choice_value = choice_value.id

            sequence_code = self._get_choice_sequence_code(choice_field, choice_value)
        else:
            sequence_code = super()._get_sequence_code()
        return sequence_code

    def _get_choice_sequence_code(self, choice_field, choice_value):
        choice_value = str(choice_value)
        code = f"{choice_field.model}.{choice_field.name}.{choice_value}"
        return self.env["ir.sequence"].next_by_code(code)
