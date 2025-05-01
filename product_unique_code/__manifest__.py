# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


{
    "name": "Product Unique Code",
    "version": "18.0.3.0.14",
    "author": "Cetmix, Loym",
    "website": "https://www.loym.com",
    "license": "LGPL-3",
    "category": "Product",
    "depends": [
        "stock", # res.config.settings
        "base_unique_code",
        "product",
    ],
    "data": [
        "data/ir_actions_server_data.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
