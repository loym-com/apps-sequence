from odoo import api, SUPERUSER_ID

def pre_init_hook(env):
    env.cr.execute("""
        ALTER TABLE ir_model
        ADD COLUMN display_name_pattern VARCHAR DEFAULT '';
    """)
