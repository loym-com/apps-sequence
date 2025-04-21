from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    crm_lead_display_name_pattern = fields.Char(
        related="ir_model_crm_lead.display_name_pattern",
        readonly=False,
        string="CRM Display Name Pattern",
    )
    crm_lead_unique_code_pattern = fields.Char(
        related="ir_model_crm_lead.unique_code_pattern",
        readonly=False,
        string="CRM Unique Code Pattern",
    )
    crm_lead_unique_code_sequence_id = fields.Many2one(
        related="ir_model_crm_lead.unique_code_sequence_id",
        readonly=False,
        string="CRM Sequence",
    )

    ir_model_crm_lead = fields.Many2one(
        "ir.model", string="CRM Model", compute="_compute_ir_model_crm_lead", store=True
    )

    @api.depends("company_id")
    def _compute_ir_model_crm_lead(self):
        for record in self:
            record.ir_model_crm_lead = self.env["ir.model"].search([("model", "=", "crm.lead")], limit=1)
