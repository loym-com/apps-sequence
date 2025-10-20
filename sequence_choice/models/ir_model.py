# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    sequence_choice_field_id = fields.Many2one(
        string="Choose sequence by",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', field_id), ('ttype', 'in', ['boolean', 'selection', 'many2one'])]",
        help="If this field is empty, "
            "all records will get a sequence code from the same sequence.\n"
            "If this field is set, "
            "a record will get a sequence code depending on the value of this field.\n"
            "Available field types are 'selection' or 'boolean'.\n"
            "A 'boolean' field has two options: True or False.\n"
            "A 'selection' field has a list of options.\n"
            "A sequence is created for each option.\n\n"
            "NB: If another Odoo app is installed later and that app adds an option,"
            "then do this to create a sequence for the new option:\n"
            "1. Set this field to empty, and save.\n"
            "2. Set this field again, and save."
    )
