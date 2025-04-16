# Copyright 2025 Loym
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sequences",
    "summary": "Each record may have a sequence code",
    "author": "Loym",
    "data": [
        "views/ir_model_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "depends": [
        "base_setup",
        "display_name", # @api.ondelete(at_uninstall=True) in base.py
    ],
    "license": "LGPL-3",
    "version": "18.0.1.0.17",
    "website": "https://www.loym.com",
}
