from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.base_display_name.tools import get_value, is_none, set_value


class UniqueCodeMixin(models.AbstractModel):
    _inherit = "x.unique.code.mixin"
