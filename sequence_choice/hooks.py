from odoo import api, SUPERUSER_ID

def pre_init_hook(env):
    env.cr.execute("""
        ALTER TABLE ir_model
        ADD COLUMN sequence_choice_field_id INTEGER REFERENCES ir_model_fields(id)
                                            ON DELETE SET NULL;
    """)
