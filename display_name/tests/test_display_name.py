import logging

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
