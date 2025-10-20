# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import psycopg2

from odoo import api, fields, models
from odoo.tools.translate import _


class UniqueCodeMixin(models.AbstractModel):
    _name = "x.unique.code.mixin"
    _description = "Unique Code Mixin"
    _inherit = "x.display.name.mixin"
    _sql_constraints = [
        (
            "unique_unique_code",
            "UNIQUE(unique_code)",
            "unique_code must be unique!",
        ),
    ]

    sequence_code = fields.Char(
        string="Sequence No.",
        copy=False,
        store=True,
    )

    unique_code = fields.Char(
        string="No.",
        copy=False,
        index=True,
        store=True,
    )
