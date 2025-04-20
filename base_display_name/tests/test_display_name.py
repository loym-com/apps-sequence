import logging

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestDisplayName(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.report_model = cls.env.ref("base.model_ir_actions_report")
        cls.report = cls.env["ir.actions.report"].create(
            {"name": "Test Report", "model": "res.partner", "report_name": "report"}
        )

    def test_1_display_name(self):
        self.report_model.display_name_pattern = ""
        self.report._invalidate_cache(["display_name"])
        self.assertEqual(self.report.display_name, "Test Report")

        self.report_model.display_name_pattern = "{id:0>5} - {name}"
        self.report._invalidate_cache(["display_name"])
        name = "Test Report"
        self.assertEqual(self.report.display_name, f"{self.report.id:0>5} - {name}")

        # Pattern with dotted field, number format and date format
        pattern = "{create_uid.id:0>3}/{create_date:%Y-%m-%d} - {name}"
        self.report_model.display_name_pattern = pattern
        self.report._invalidate_cache(["display_name"])
        self.assertEqual(
            self.report.display_name, pattern.format(
                create_uid=self.report.create_uid,
                create_date=self.report.create_date,
                name=self.report.name,
            )
        )

    def test_2a_invalid_display_name_pattern(self):
        self.env.cr.execute(
            f"UPDATE ir_model "
            f"SET display_name_pattern = '{{invalid_field}}'"
            f"WHERE id = {self.report_model.id};"
        )
        self.report._invalidate_cache(["display_name"])
        self.assertEqual(self.report.display_name, "Test Report")

    def test_2b_set_invalid_display_name_pattern(self):
        with self.assertRaises(ValidationError):
            self.report_model.display_name_pattern = "{invalid_field}"

    def test_3a_false_boolean(self):
        self.report.multi = False
        self.report_model.display_name_pattern = "{multi}"
        self.report._invalidate_cache(["display_name"])
        self.assertEqual(self.report.display_name, "False")

    def test_3b_false_char(self):
        self.report.path = False
        self.report_model.display_name_pattern = "{path}"
        self.report._invalidate_cache(["display_name"])
        self.assertEqual(self.report.display_name, "Test Report")
