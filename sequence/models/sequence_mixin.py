from odoo import models, fields


class SequenceMixin(models.AbstractModel):
    _name = "sequence.mixin"
    _description = "Sequence Mixin"
    _sql_constraints = [
        (
            "sequence_mixin_unique_sequence_code",
            "UNIQUE(sequence_code)",
            "Sequence code must be unique",
        ),
    ]

    sequence_code = fields.Char(string="Sequence Code", readonly=True, copy=False)
