Sequences
=========

**EDIT**

`display_name` and `project_display` replace all `sequence` modules.

`display_name` has **display_code** (computed), and a mixin to store it.

`project_display` uses the mixin. Then **display_code_pattern** is visible in ir.model.

**Original**

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

Sequences seem to be implemented in many OCA modules on a supported version (16-18):

1. account_analytic_sequence
2. account_journal_general_sequence
3. account_move_name_sequence
4. account_sequence_option
5. base_partner_sequence
6. base_sequence_default
7. base_sequence_option
8. hr_expense_advance_clearing_sequence
9. hr_expense_sequence
10. hr_expense_sequence_option
11. l10n_th_base_sequence
12. maintenance_equipment_sequence
13. maintenance_request_sequence
14. mrp_workorder_sequence
15. product_default_code_res_company_code
16. product_internal_reference_generator
17. product_lot_sequence
18. product_sequence
19. project_task_code
20. purchase_order_line_sequence
21. repair_type_sequence
22. sale_order_line_sequence
23. sale_quotation_number
24. sale_stock_line_sequence
25. sequence_check_digit
26. sequence_python
27. sequence_reset_period
28. stock_picking_line_sequence

I want `sequence` and `display_name` to be generic
so that they can be useful and easy to implement for various sequences.
[Here I have opened an issue to discuss these things](https://github.com/OCA/server-ux/issues/1058),
before I make pull requests to the OCA.

BTW: `sequence_choice` is a new module, allowing multiple sequences for a model.
