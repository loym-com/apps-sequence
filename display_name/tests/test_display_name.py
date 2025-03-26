import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestDisplayName(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env.ref("base.model_res_partner")
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test Contact", "ref": "TEST"}
        )

    def test_1_display_name(self):
        self.assertEqual(self.partner.display_name, "Test Contact")
        self.partner_model.display_name_pattern = "%(ref)s - %(name)s"
        self.assertEqual(self.partner.display_name, "TEST - Test Contact")
