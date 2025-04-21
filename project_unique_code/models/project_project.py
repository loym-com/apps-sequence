from odoo import api, fields, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "unique.code.mixin"]

    name = fields.Char(
        # We actually require it with the SQL constraint, but it is disabled
        # here to let users create/write projects without name, and let this module
        # add a default name if needed
        required=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res._sync_analytic_account_name()
        return res

    def write(self, vals):
        super().write(vals)
        self._sync_analytic_account_name()
        return True

    def _sync_analytic_account_name(self):
        """Set analytic account name equal to project's display name."""
        for rec in self:
            if not rec.account_id:
                continue
            rec.account_id.name = rec.display_name
