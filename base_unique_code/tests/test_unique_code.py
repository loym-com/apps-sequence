import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestUniqueCode(TransactionCase):

    @classmethod
    def _get_field(cls, model_id, field_name):
        return cls.env["ir.model.fields"].search(
            [("model_id", "=", model_id), ("name", "=", field_name)]
        ).ensure_one()

    def setUp(self):
        super().setUp()
        # Sequence must be reset to 1, otherwise the tests will fail
        sequence = self.env["ir.sequence"].create(
            [
                {
                    "name": "Test Partner Sequence",
                    "prefix": "partner-",
                    "padding": 5,
                    "number_increment": 1,
                }
            ]
        )
        self.model = self.env.ref("base.model_res_partner")
        self.model.unique_code_pattern = "{__sequence__}"
        self.model.unique_code_sequence_id = sequence.id

    def test_0_sequence(self):
        self.model.unique_code_pattern = ""
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.unique_code, False)
        self.assertEqual(record.name, "Test Partner")

    def test_1_secuence(self):
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.unique_code, "partner-00001")
        record.unique_code = ""
        self.assertEqual(record.unique_code, "")
        record.set_unique_code_and_name()
        self.assertEqual(record.unique_code, "partner-00002")

    def test_no_change_of_existing_sequence_code(self):
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.unique_code, "partner-00001")
        record.set_unique_code_and_name()
        self.assertEqual(record.unique_code, "partner-00001")

    def test_no_name_get_next_sequence_code(self):
        # Contact name is mandatory except when type == "other"
        record = self.env[self.model.model].create({"type": "other"})
        self.assertEqual(record.name, "partner-00001")
