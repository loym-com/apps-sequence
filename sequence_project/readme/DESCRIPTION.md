This addon with dependencies
has all features of `project_sequence` and `project_task_code`.
Generic features are moved to `sequence`.

Important changes:

- Settings are in *Settings \> Technical \> Database Structure \> Models*.
- Licence is AGPL-3 (`project_sequence` has LGPL-3)
- Project ir.sequence code: "project.sequence" -> "project.project".
- Task field: "code" -> "sequence_code".
- Task "sequence_code" is not required. No pre_init_hook.
- Task "sequence_code" must be unique, not just unique per company.
  (Alternative: Project "sequence_code" is not unique, just per company.)
- Task "sequence_code" is not auto-filled with post_init_hook. Allow to customize the sequence first. Then select tasks, click Action menu, Set Sequence Code.
- Views are updated (id, name etc.).
- Translations are not copied for now.

`project_sequence`
Add a sequence field to projects, filled automatically and add a code
sequence filter in tree view project.

`project_task_code`
This module adds a sequential code for tasks.
