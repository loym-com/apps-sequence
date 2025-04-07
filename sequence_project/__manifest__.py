# Copyright 2025 Loym AS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sequence for projects and tasks",
    "summary": "",
    "author": "Loym AS",
    "data": [
        "views/project_project_views.xml",
        "views/project_task_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "depends": [
        "display_name",
        "project",
        "sequence",
    ],
    "license": "AGPL-3",
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "version": "18.0.1.0.5",
    "website": "https://www.loym.com",
}
