This module depends on `sequence` which numbers records with a sequence per model.
But you may want to have multiple sequences for the same model.
E.g. you want separate numbering for companies and people.
The contact model has a 'company_type' field which can be 'person' or 'company'.
With this module, you can configure that the sequence code for a contact will
consider the 'company_type', or another 'selection' or 'boolean' field.
There will be a sequence for each option.
