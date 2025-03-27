from odoo import api, SUPERUSER_ID

def post_init_hook(env):
    Project = env["project.project"]
    Task = env["project.task"]

    Project.set_display_name_pattern("%(sequence_code)s - %(name)s")
    Task.set_display_name_pattern("[%(sequence_code)s] %(name)s")

    Project.set_sequence_values(
        {
            "prefix": "%(y)s-",
            "use_date_range": True,
            "padding": 5,
            "company_id": False,
        }
    )
    Task.set_sequence_values(
        {
            "prefix": "T",
            "padding": 4,
            "company_id": False,
        }
    )
