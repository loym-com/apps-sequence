from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_template_display_name_pattern = fields.Char(
        related="ir_model_product_template.display_name_pattern",
        readonly=False,
        string="Template Display Name Pattern",
    )
    product_template_unique_code_pattern = fields.Char(
        related="ir_model_product_template.unique_code_pattern",
        readonly=False,
        string="Template Unique Code Pattern",
    )
    product_template_unique_code_sequence_id = fields.Many2one(
        related="ir_model_product_template.unique_code_sequence_id",
        readonly=False,
        string="Template Sequence",
    )
    product_template_unique_code_from_variant = fields.Boolean(
        string="Get Unique Code from Variant",
        config_parameter="product_unique_code.product_template_unique_code_from_variant"
    )

    product_product_display_name_pattern = fields.Char(
        related="ir_model_product_product.display_name_pattern",
        readonly=False,
        string="Variant Display Name Pattern",
    )
    product_product_unique_code_pattern = fields.Char(
        related="ir_model_product_product.unique_code_pattern",
        readonly=False,
        string="Variant Unique Code Pattern",
    )
    product_product_unique_code_sequence_id = fields.Many2one(
        related="ir_model_product_product.unique_code_sequence_id",
        readonly=False,
        string="Variant Sequence",
    )

    ir_model_product_template = fields.Many2one(
        "ir.model", string="Template Model", compute="_compute_ir_model_product_template", store=True
    )
    ir_model_product_product = fields.Many2one(
        "ir.model", string="Variant Model", compute="_compute_ir_model_product_product", store=True
    )

    @api.depends("company_id")
    def _compute_ir_model_product_template(self):
        for record in self:
            record.ir_model_product_template = self.env["ir.model"].search([("model", "=", "product.template")], limit=1)

    @api.depends("company_id")
    def _compute_ir_model_product_product(self):
        for record in self:
            record.ir_model_product_product = self.env["ir.model"].search([("model", "=", "product.product")], limit=1)
