from odoo import models

def get_value(item, field):
    """ Get a value in a record or dict.
        item: record or dict
        field: field name to get value
        Returns: value (None if not found in dict - or if record value is falsy)
    """
    if isinstance(item, dict):
        if field in item:
            return item[field]
    elif isinstance(item, models.BaseModel):
        value = getattr(item, field)
        if (
            value or
            isinstance(value, models.BaseModel) or
            item._fields[field].type == "boolean"
        ):
            return value
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
