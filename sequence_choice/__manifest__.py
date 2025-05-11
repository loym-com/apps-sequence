# Copyright 2025 Loym
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "sequence_choice",
    "summary": "Unique code depends on a field",
    "author": "Loym",
    "data": [
        "views/ir_model_views.xml",
    ],
    "depends": ["base_unique_code"],
    "excludes": ["project_internal_external"],
    "license": "LGPL-3",
    "pre_init_hook": "pre_init_hook",
    "version": "18.0.3.0.17",
    "website": "https://www.loym.com",
}
