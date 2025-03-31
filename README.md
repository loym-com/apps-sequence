=========
Sequences
=========

`sequence` and `display_name` are based on `project_sequence` and `project_task_code`.

- `ir.model` has 2 new fields to store *sequence field* and *display name pattern*.
- Settings - General Settings - Permissions has two checkboxes to show these fields.
- These fields enable administrators to set a sequence for each model.

`sequence_project` is also based on `project_sequence` and `project_task_code`.
It shows how one may implement a sequence for a model:

- The module should depend on `sequence`.
- Inherit "sequence.mixin"
- Add views to show the sequence_code.
- Optionally, depend on `display_name`.
- Use a post_init_hook to set a default sequence and display_name_pattern.
- Use "res.config.settings" to let the user set a custom display_name_pattern.
  Save the pattern to "ir.model" (not "ir.config_parameter").

`sequence` and `display_name` are made with two use cases in mind:

1. A developer may depend on them in a sequence module.
2. A database admin may configure sequences and display names directly in the UI.

To combine these use cases,
settings should be stored in `ir.model` (instead of `ìr.config_parameter`).

Sequences are already implemented in ca 30 OCA modules on a supported version (16-18):

* account_analytic_sequence
* account_journal_general_sequence
* account_move_name_sequence
* account_sequence_option
* base_partner_sequence
* base_sequence_default
* base_sequence_option
* hr_expense_advance_clearing_sequence
* hr_expense_sequence
* hr_expense_sequence_option
* l10n_th_base_sequence
* maintenance_equipment_sequence
* maintenance_request_sequence
* mrp_workorder_sequence
* product_default_code_res_company_code
* product_internal_reference_generator
* product_lot_sequence
* product_sequence
* project_task_code
* purchase_order_line_sequence
* repair_type_sequence
* sale_order_line_sequence
* sale_quotation_number
* sale_stock_line_sequence
* sequence_check_digit
* sequence_python
* sequence_reset_period
* stock_picking_line_sequence

I want `sequence` and `display_name` to be generic
so they can be useful and easy to implement for various sequences.
[Here I have opened an issue to discuss these things](https://github.com/OCA/server-ux/issues/1058),
before I make pull requests to the OCA.

BTW: `sequence_choice` is a new module, allowing multiple sequences for a model.
