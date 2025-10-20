import logging
import psycopg2
import re

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.translate import _

from odoo.addons.base_display_name.tools import get_value, is_none, set_value, get_indexed_pattern

_logger = logging.getLogger(__name__)


class DisplayNameMixin(models.AbstractModel):
    _name = "x.display.name.mixin"
    _description = "x.display.name.mixin"
