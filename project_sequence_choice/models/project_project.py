# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.model_create_multi
    def create(self, vals_list):
        seq_field = self.env["res.config.settings"]._get_project_sequence_field()
        if seq_field:
            for vals in vals_list:
                seq_field_value = vals.get(seq_field.name)
                sequence_code = self._get_next_sequence_code(seq_field, seq_field_value)
                vals["sequence_code"] = sequence_code
        res = super().create(vals_list)
        res._sync_analytic_account_name()
        return res

    def set_sequence_code(self):
        seq_field = self.env["res.config.settings"]._get_project_sequence_field()
        for project in self:
            if seq_field:
                seq_field_value = getattr(project, seq_field.name)
                sequence_code = self._get_next_sequence_code(seq_field, seq_field_value)
            else:
                sequence_code = self.env["ir.sequence"].next_by_code("project.sequence")
            project.sequence_code = sequence_code

    def _get_next_sequence_code(self, seq_field, seq_field_value):
        if seq_field_value == True:
            seq_field_value = "yes"
        elif seq_field_value == False:
            seq_field_value = "no"
        # Code of sequence
        code = f"{seq_field.model}.{seq_field.name}.{seq_field_value}"
        # Project sequence_code
        return self.env["ir.sequence"].next_by_code(code)
