from odoo import api, fields, models
from odoo.exceptions import UserError


class UniqueCodeMixin(models.AbstractModel):
    _inherit = "x.unique.code.mixin"
