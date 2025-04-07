from odoo import api, SUPERUSER_ID

def post_init_hook(env):
    project_model = env["ir.model"].sudo().search([("model", "=", "project.project")])
    task_model = env["ir.model"].sudo().search([("model", "=", "project.task")])

    if not project_model.display_name_pattern:
        project_model.display_name_pattern = "{display_code} - {name}"
    if not task_model.display_name_pattern:
        task_model.display_name_pattern ="{display_code} - {name}"

    if not project_model.display_code_pattern:
        project_model.display_code_pattern = "P{id:>03}"
    if not task_model.display_code_pattern:
        task_model.display_code_pattern = "T{id:>05}"

# def uninstall_hook(env):
#     """
#     Uninstall hook to remove the custom display name pattern and sequence.
#     """
#     project_model = env["ir.model"].sudo().search([("model", "=", "project.project")])
#     task_model = env["ir.model"].sudo().search([("model", "=", "project.task")])

#     project_model.display_name_pattern = False
#     project_model.display_code_pattern = False
#     task_model.display_name_pattern = False
#     task_model.display_code_pattern = False
