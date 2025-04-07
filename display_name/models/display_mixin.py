from odoo import api, fields, models


class DisplayMixin(models.AbstractModel):
    _name = "display.mixin"
    _description = "Display Mixin"
    _sql_constraints = [
        (
            "unique_display_code_per_company",
            "UNIQUE(display_code, company_id)",
            "Display Code must be unique per company!",
        ),
    ]

    display_code = fields.Char(store=True)
