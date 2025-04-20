# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import psycopg2

from odoo import api, fields, models
from odoo.tools.translate import _

def get_value(item, field):
    """ Get a value in a record or dict.
        item: record or dict
        field: field name to get value
        Returns: value (None if not found in dict, or if record value is falsy)
    """
    if isinstance(item, dict):
        if field in item:
            return item[field]
        else:
            return None
    elif isinstance(item, models.BaseModel):
        return getattr(item, field, None)
    else:
        raise ValueError(f"Invalid type: {type(item)}")

def is_none(item, field):
    return get_value(item, field) is None

def set_value(item, field, value):
    """ Set a value in a record or dict.
        item: record or dict
        field: field name to set value
    """
    if isinstance(item, dict):
        item[field] = value
    elif isinstance(item, models.BaseModel):
        setattr(item, field, value)
    else:
        raise ValueError(f"Invalid type: {type(item)}")


class Base(models.AbstractModel):
    _inherit = "base"
    _sql_constraints = [
        (
            "unique_code",
            "UNIQUE(unique_code)",
            "unique_code must be unique!",
        ),
    ]

    unique_code = fields.Char(copy=False, index=True)

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = self.set_unique_code_and_name(vals_list)
        return super().create(vals_list)

    def write(self, vals):
        super().write(vals)
        self._set_name_if_empty()

    def set_unique_code_and_name(self, vals_list=None):
        vals_list = self._set_unique_code(vals_list)
        vals_list = self._set_name_if_empty(vals_list)
        return vals_list

    def _set_unique_code(self, vals_list=None):
        return self._set_field_from_pattern(
            "unique_code", "unique_code_pattern", vals_list
        )
    
    def _set_name_if_empty(self, vals_list=None):
        """Set name = unique_code if removing name or no existing name

        Checking if the record has a name may affect the performance..."""

        # Relevant for uninstalling the module
        context = self.env.context
        if "prefetch_fields" in context and not context.get("prefetch_fields"):
            return vals_list

        if "name" not in self._fields:
            return vals_list

        model = self._get_ir_model()
        pattern = model.unique_code_pattern
        if not pattern:
            return vals_list

        # Handle both create and write
        for item in vals_list or self:
            if get_value(item, "unique_code") and is_none(item, "name"):
                set_value(item, "name", item["unique_code"])
        return vals_list


    # def set_sequence_code(self, vals_list=None):
    #     model = self.env["ir.model"].sudo().search([("model", "=", self._name)])
    #     # if "sequence_code_field_id" in model._fields and model.sequence_code_field_id:
    #     if model.sequence_code_field_id:
    #         FieldSudo = self.env["ir.model.fields"].sudo()
    #         field = FieldSudo.browse(model.sequence_code_field_id.id)
    #         if vals_list:
    #             # create
    #             for vals in vals_list:
    #                 if field.name not in vals:
    #                     # sequence code (sequence_choice needs vals)
    #                     vals[field.name] = self._get_next_sequence_code(vals)
    #                     # name (if empty)
    #                     if "name" in self._fields and not vals.get("name"):
    #                         vals["name"] = vals[field.name]
    #         else:
    #             # write
    #             for record in self:
    #                 if not getattr(record, field.name):
    #                     # sequence code (sequence_choice needs vals)
    #                     setattr(record, field.name, record._get_next_sequence_code())
    #                     # name (if empty)
    #                     if "name" in self._fields and not record.name:
    #                         record.name = getattr(record, field.name)
    #     return vals_list

    # def _get_next_sequence_code(self, vals=None):
    #     "vals is needed by sequence_choice to read values of a record to be created."
    #     return self.env["ir.sequence"].next_by_code(self._name)



    # Override methods in base_display_name to avoid checking __sequence__.

    def _get_display_value(self, item, field_path):
        """Use sequence if:
        1) field_path is "__sequence__"
        2) ir.model has unique_code_sequence_id
        """
        if field_path == "__sequence__" and is_none(item, "unique_code"):
            sequence = self._get_ir_model(prefetch_fields=False).unique_code_sequence_id
            if sequence:
                return (sequence.next_by_id(), "char")
        return super()._get_display_value(item, field_path)

    def _is_valid_display_field_paths(self, field_paths):
        """Do not check __sequence__."""
        field_paths = [item for item in field_paths if item != "__sequence__"]
        return super()._is_valid_display_field_paths(field_paths)
