# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    project_sequence_multi_field = fields.Many2one(
        string="Project Sequence Field",
        comodel_name="ir.model.fields",
        domain="""[
            ('model_id', '=', 'project.project'),
            ('required', '=', True),
            ('ttype', 'in', ['boolean', 'selection']),
        ]""",
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        field = self._get_project_sequence_field()
        if field:
            res['project_sequence_multi_field'] = field.id
        else:
            res['project_sequence_multi_field'] = False
        return res
    
    def _get_project_sequence_field(self):
        # model_name.field_name -> field.id
        field = False
        model_field = self.env['ir.config_parameter'].sudo().get_param('project_sequence_multi_field', default=False)
        if model_field:
            model_name, field_name = model_field.rsplit('.', 1)
            field = self.env['ir.model.fields'].search(
                [
                    ('model_id.model', '=', model_name),
                    ('name', '=', field_name),
                ],
            ).ensure_one()
        return field

    @api.model
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        # field.id -> model_name.field_name
        field = self.project_sequence_multi_field
        if field:
            model_field = f"{field.model}.{field.name}"
        else:
            model_field = ""
        Parameter = self.env['ir.config_parameter']
        Parameter.sudo().set_param('project_sequence_multi_field', model_field)
        self._create_project_sequences(model_field)

    def _create_project_sequences(self, model_field):
        Sequence = self.env["ir.sequence"]
        field = self.project_sequence_multi_field
        if field:
            if field.ttype == 'boolean':
                seq_field_values = ["yes", "no"]
            elif field.ttype == 'selection':
                seq_field_values = field.selection_ids.mapped("value")
            for value in seq_field_values:
                code = f"{model_field}.{value}"
                seq = Sequence.search([('code', '=', code)])
                if not seq:
                    seq = Sequence.create({
                        'name': code,
                        'code': code,
                        'padding': 5,
                        'prefix': value + "-",
                    })
                    _logger.info(f"Created sequence {seq.name}")
