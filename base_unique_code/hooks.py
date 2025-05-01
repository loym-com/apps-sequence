from odoo import api, SUPERUSER_ID

def pre_init_hook(env):
    try:
        env.cr.execute("""
            ALTER TABLE ir_model
            ADD COLUMN unique_code_pattern VARCHAR DEFAULT '';
        """)
    except Exception:
        pass
