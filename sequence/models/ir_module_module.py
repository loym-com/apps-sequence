# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def button_immediate_uninstall(self):
        """Override to set a context variable during uninstallation."""
        # Set the 'uninstall_mode' context key to True. Used in base write()
        return super(
            IrModuleModule, self.with_context(uninstall_mode=True)
        ).button_immediate_uninstall()
