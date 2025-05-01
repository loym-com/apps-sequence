from odoo import api, SUPERUSER_ID
from odoo.exceptions import ValidationError

def pre_init_hook(env):
    module = env["ir.module.module"].search(
        [("name", "=", "project_internal_external")], limit=1
    )
    if module and module.state == "installed":
        raise ValidationError(
            "Uninstall 'project_internal_external' before installing 'sequence_choice'."
        )
