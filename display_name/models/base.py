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
        search_fnames = self._get_display_name_field_paths()
        if not search_fnames:
            return super()._search_display_name(operator, value)

        # Copied from ORM models.py
        if operator.endswith('like') and not value and '=' not in operator:
            # optimize out the default criterion of ``like ''`` that matches everything
            # return all when operator is positive
            return expression.FALSE_DOMAIN if operator in expression.NEGATIVE_TERM_OPERATORS else expression.TRUE_DOMAIN
        aggregator = expression.AND if operator in expression.NEGATIVE_TERM_OPERATORS else expression.OR
        return aggregator([[(field_name, operator, value)] for field_name in search_fnames])
    
    @api.depends(lambda self: self._get_display_name_field_paths())
    def _compute_display_name(self):

        def get_nested_field_value(field_path):
            fields = field_path.split('.')
            value = record
            try:
                for field in fields:
                    value = getattr(value, field)
                return str(value)
            except AttributeError:
                return None

        def values_are_non_empty_and_different(values):
            non_empty = [value for value in values.values() if bool(value)]
            if len(non_empty) != len(values):
                return False
            if len(set(non_empty)) != len(non_empty):
                return False
            return True
        
        res = super()._compute_display_name()

        Model = self.env["ir.model"]
        # Order by a field which always exists, to install apps without errors.
        model = Model.sudo().search([("model", "=", self._name)], order="id")

        pattern = model._get_display_name_pattern()
        if not pattern:
            return res

        field_paths = model._get_display_name_field_paths()
        if not field_paths:
            return res

        for record in self:
            values = {
                field_path: get_nested_field_value(field_path)
                for field_path in field_paths
            }
            if values_are_non_empty_and_different(values):
                record.display_name = pattern.format(**values)

    def _get_display_name_field_paths(self):
        Model = self.env["ir.model"]
        return Model.search([("name", "=", self._name)])._get_display_name_field_paths()
