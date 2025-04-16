import logging

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestDisplayName(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_model = cls.env.ref("base.model_res_groups")
        cls.group = cls.env["res.groups"].create(
            {"name": "Test Group"}
        )

    def test_1_display_name(self):
        self.group_model.display_name_pattern = ""
        self.group._invalidate_cache(["display_name"])
        self.assertEqual(self.group.display_name, "Test Group")

        self.group_model.display_name_pattern = "{id:>05} - {name}"
        self.group._invalidate_cache(["display_name"])
        self.assertEqual(self.group.display_name, f"{self.group.id:>05} - Test Group")

        # Pattern with dotted field, number format and date format
        pattern = "{create_uid.id:>03}/{create_date:%Y-%m-%d} - {name}"
        self.group_model.display_name_pattern = pattern
        self.group._invalidate_cache(["display_name"])
        self.assertEqual(
            self.group.display_name, pattern.format(
                create_uid=self.group.create_uid,
                create_date=self.group.create_date,
                name=self.group.name,
            )
        )

    def test_invalid_display_name_pattern(self):
        self.env.cr.execute(
            f"UPDATE ir_model "
            f"SET display_name_pattern = '{{invalid_field}}'"
            f"WHERE id = {self.group_model.id};"
        )
        self.group._invalidate_cache(["display_name"])
        self.assertEqual(self.group.display_name, "Test Group")

    def test_set_invalid_display_name_pattern(self):
        with self.assertRaises(ValidationError):
            self.group_model.display_name_pattern = "{invalid_field}"
