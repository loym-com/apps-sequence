import logging
import psycopg2
import re

from odoo import api, models
from odoo.osv import expression
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _search_display_name(self, operator, value):
        search_fnames = self._get_display_name_field_names()
        if not search_fnames:
            return super()._search_display_name(operator, value)

        # Copied from ORM models.py
        if operator.endswith('like') and not value and '=' not in operator:
            # optimize out the default criterion of ``like ''`` that matches everything
            # return all when operator is positive
            return expression.FALSE_DOMAIN if operator in expression.NEGATIVE_TERM_OPERATORS else expression.TRUE_DOMAIN
        aggregator = expression.AND if operator in expression.NEGATIVE_TERM_OPERATORS else expression.OR
        return aggregator([[(field_name, operator, value)] for field_name in search_fnames])
    
    @api.depends(lambda self: self._get_display_name_field_names())
    def _compute_display_name(self):

        def fields_exist_and_are_filled_and_different(field_values):
            # Check if there are any fields
            if not field_values:
                return False
            # Check if all fields have a non-empty value
            if not all(field_values.values()):
                return False
            # Check if all values are different
            values = list(field_values.values())
            if len(values) != len(set(values)):
                return False
            return True
        
        res = super()._compute_display_name()

        Model = self.env["ir.model"]
        # Order by a field which always exists, to install apps without errors.
        model = Model.sudo().search([("model", "=", self._name)], order="id")

        pattern = model._get_display_name_pattern()
        if not pattern:
            return res

        field_names = model._get_display_name_field_names()
        for record in self:
            field_values = {
                field_name: getattr(record, field_name, "")
                for field_name in field_names
            }
            if fields_exist_and_are_filled_and_different(field_values):
                record.display_name = pattern.format(**field_values)

    def _get_display_name_field_names(self):
        Model = self.env["ir.model"]
        return Model.search([("name", "=", self._name)])._get_display_name_field_names()
