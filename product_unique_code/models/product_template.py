# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "x.unique.code.mixin"]

    unique_code = fields.Char(
        string="Product Number",
        store=True,
    )
    main_variant_id = fields.Many2one(
        comodel_name="product.product",
        string="Main Variant",
        # group="stock.group_stock_manager",
        help="The main variant of the product template. "
             "This is used to determine the unique code for the product template. "
             "Only STOCK MANAGER can change this value.",
    )
