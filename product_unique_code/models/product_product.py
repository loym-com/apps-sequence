from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "unique.code.mixin"]
