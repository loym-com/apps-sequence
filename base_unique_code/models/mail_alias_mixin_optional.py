from odoo import api, fields, models

class AliasMixinOptional(models.AbstractModel):
    _inherit = "mail.alias.mixin.optional"

    # Copied from mail
    def _alias_filter_fields(self, values, filters=False):
        """ Split the vals dict into two dictionnary of vals, one for alias
        field and the other for other fields """
        if not filters:
            filters = self.env['mail.alias']._fields.keys()
            # NEW
            filters = list(filters)
            filters.remove("unique_code")
            # END NEW
        alias_values, record_values = {}, {}
        for fname in values.keys():
            if fname in filters:
                alias_values[fname] = values.get(fname)
            else:
                record_values[fname] = values.get(fname)
        return alias_values, record_values
