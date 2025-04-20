# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    unique_code = fields.Char(
        string="Product Number",
        compute="_compute_unique_code",
        store=True,
    )

    @api.depends("product_variant_ids.unique_code", "product_variant_ids.active")
    def _compute_unique_code(self):
        """Get active product variant unique_code."""
        for template in self:
            product = template.product_variant_ids.filtered(lambda p: p.active)
            if product:
                product = fields.first(product)
                template.unique_code = product.unique_code
