from openupgradelib import openupgrade


def pre_init_hook(env):
    app = "sequence_project"
    openupgrade.add_fields(
        env,
        [
            ("sequence_code", 'project.project', 'project_project', 'char', False, app),
            ("sequence_code", 'project.task', 'project_task', 'char', False, app),
        ],
    )

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
