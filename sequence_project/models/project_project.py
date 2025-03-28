from odoo import api, fields, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "sequence.mixin"]
    _sql_constraints = [
        (
            "unique_sequence_code",
            "UNIQUE(sequence_code)",
            "Sequence code must be unique!",
        ),
    ]

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


    def write(self, vals):
        """Sync name and analytic account name when name is changed."""
        # If name isn't changing, nothing special to do
        if "name" not in vals and "sequence_name" not in vals:
            return super().write(vals)
        # When changing name, we need to update the analytic account name too
        for one in self:
            sequence_code = vals.get("sequence_code", one.sequence_code)
            name = vals.get("name") or sequence_code
            super().write(dict(vals, name=name))
        self._sync_analytic_account_name()
        return True