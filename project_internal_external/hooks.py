from odoo import api, SUPERUSER_ID
from odoo.exceptions import ValidationError

def pre_init_hook(env):
    module = env["ir.module.module"].search([("name", "=", "sequence_choice")], limit=1)
    if module and module.state == "installed":
        raise ValidationError(
            "Uninstall 'sequence_choice' before installing 'project_internal_external'."
        )
