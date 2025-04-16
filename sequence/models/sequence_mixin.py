from odoo import models, fields


class SequenceCodeMixin(models.AbstractModel):
    _name = "sequence.code.mixin"
    _description = "Sequence Code Mixin"
    _sql_constraints = [
        (
            "unique_sequence_code_per_company",
            "UNIQUE(sequence_code, company_id)",
            "Sequence code must be unique per company!",
        ),
    ]

    sequence_code = fields.Char(string="Sequence Code", readonly=True, copy=False)
