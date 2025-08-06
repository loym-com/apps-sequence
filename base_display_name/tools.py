import re

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

def get_indexed_pattern(pattern, field_paths):
    """Replace field paths with their index.
    Example: "{related_id.field} {name}" -> "{0} {1}"
    """
    def replace_path_with_index(match):
        full_placeholder = match.group(0)
        field_path = match.group(1)
        format_spec = match.group(2) or ""
        if field_path in field_paths:
            return f"{{{field_paths.index(field_path)}{format_spec}}}"
        else:
            return full_placeholder
    return re.sub(r"\{([\w.]+)(:[^}]*)?\}", replace_path_with_index, pattern)
