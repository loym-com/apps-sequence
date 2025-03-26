from odoo import models, fields


class SequenceMixin(models.AbstractModel):
    _name = "sequence.mixin"
    _description = "Sequence Mixin"
    _sql_constraints = [
        (
            "unique_sequence_code_per_company",
            "UNIQUE(sequence_code, company_id)",
            "Sequence code must be unique per company",
        ),
    ]

    sequence_code = fields.Char(string="Sequence Code", readonly=True, copy=False)

    def set_display_name_pattern(self, display_name_pattern=None):
        model = self.env["ir.model"].search(domain=[("model", "=", self._name)])
        if not model.display_name_pattern:
            default_pattern = "%(sequence_code)s - %(name)s"
            model.display_name_pattern = display_name_pattern or default_pattern

    def set_sequence_values(self, sequence_values=None):
        model = self.env["ir.model"].search(domain=[("model", "=", self._name)])
        field = self.env["ir.model.fields"].search(
            [("model_id", "=", model.id), ("name", "=", "sequence_code")]
        )

        def get_one_sequence():
            return self.env["ir.sequence"].search([("code", "=", model.model)])
        sequence = get_one_sequence()

        # Model: Set sequence code field (will create sequence(s) if missing)
        model.sequence_code_field_id = field.id

        # Sequence: if one new: set values
        if sequence_values and not sequence:
            sequence = get_one_sequence()
            if sequence:
                sequence.write(sequence_values)
