from odoo import api, SUPERUSER_ID


def pre_init_hook(env):
    env.cr.execute("""
        ALTER TABLE project_project
        ADD COLUMN sequence_code VARCHAR DEFAULT '';
        ALTER TABLE project_task
        ADD COLUMN sequence_code VARCHAR DEFAULT '';
    """)

def post_init_hook(env):
    project_model = env["ir.model"].sudo().search([("model", "=", "project.project")])
    task_model = env["ir.model"].sudo().search([("model", "=", "project.task")])

    project_model.display_name_pattern = "{sequence_code} - {name}"
    task_model.display_name_pattern ="[{sequence_code}] {name}"

    project_model.set_sequence(
        field_name="sequence_code",
        sequence_values={
            "prefix": "%(y)s-",
            "use_date_range": True,
            "padding": 5,
            "company_id": False,
        }
    )
    task_model.set_sequence(
        field_name="sequence_code",
        sequence_values={
            "prefix": "T",
            "padding": 4,
            "company_id": False,
        }
    )

def uninstall_hook(env):
    """
    Uninstall hook to remove the custom display name pattern and sequence.
    """
    project_model = env["ir.model"].sudo().search([("model", "=", "project.project")])
    task_model = env["ir.model"].sudo().search([("model", "=", "project.task")])

    project_model.display_name_pattern = False
    task_model.display_name_pattern = False
