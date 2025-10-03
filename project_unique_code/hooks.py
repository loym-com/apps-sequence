def post_init_hook(env):
    # Default project display name pattern
    pattern = "{r.unique_code}{' ' if r.unique_code != r.name}{r.name if r.unique_code != r.name}"
    env["ir.model"].search([("model", "=", "project.project")]).display_name_pattern = pattern
