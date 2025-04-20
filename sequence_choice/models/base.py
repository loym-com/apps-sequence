from odoo import api, fields, models


class Base(models.AbstractModel):
    _inherit = "base"

    def _get_display_value_and_type(self, item, field_path):
        """Use sequence if:
        1) field_path is "__sequence__"
        2) ir.model has sequence_choice_field_id
        """
        if field_path == "__sequence__":
            fld_id = self._get_ir_model(prefetch_fields=False).sequence_choice_field_id
            if fld_id:
                choice_field = self.env["ir.model.fields"].browse(fld_id)
                choice_value = getattr(self, choice_field.name)
                # if choice_field.ttype == "many2one":
                #     choice_value = choice_value.id
                choice_value = str(choice_value)
                code = f"{choice_field.model}.{choice_field.name}.{choice_value}"
                return (self.env["ir.sequence"].next_by_code(code), "char")
        return super()._get_display_value_and_type(item, field_path)
