import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestSequence(TransactionCase):

    @classmethod
    def _get_field(cls, model_id, field_name):
        return cls.env["ir.model.fields"].search(
            [("model_id", "=", model_id), ("name", "=", field_name)]
        ).ensure_one()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # normal
        cls.model_0 = cls.env.ref("base.model_ir_attachment")
        # code
        cls.model_1 = cls.env.ref("base.model_res_partner_title")
        cls.model_1.sequence_code_field_id = cls._get_field(cls.model_1.id, "shortcut").id
        # code, boolean
        cls.model_2b = cls.env.ref("base.model_res_groups")
        cls.model_2b.sequence_code_field_id = cls._get_field(cls.model_2b.id, "comment").id
        cls.model_2b.sequence_selection_field_id = cls._get_field(cls.model_2b.id, "share").id
        # code, many2one
        cls.model_2m = cls.env.ref("base.model_res_partner")
        cls.model_2m.sequence_code_field_id = cls._get_field(cls.model_2m.id, "ref").id
        cls.model_2m.sequence_selection_field_id = cls._get_field(cls.model_2m.id, "title").id
        # code, selection - see test_3_sequence_selection

    def test_1_action(self):
        action = self.env["ir.actions.server"].search(
            [
                ("model_id", "=", self.model_1.id),
                ("binding_model_id", "=", self.model_1.id),
                ("usage", "=", "ir_actions_server"),
                ("state", "=", "code"),
                ("name", "=", "Set Sequence"),
            ]
        )
        self.assertTrue(action)

    def test_2_sequences(self):
        _logger.info(f"test_2_sequences: self.model_0.model = {self.model_0.model}")
        test0 = self.env[self.model_0.model].create({"name": "Test Attachment"})
        self.assertEqual(test0.name, "Test Attachment")

        test1 = self.env[self.model_1.model].create({"name": "Test Partner Title"})
        self.assertEqual(test1.shortcut, "title-00001")
        test1.shortcut = ""
        self.assertEqual(test1.shortcut, "")
        test1.sequence_code_set()
        self.assertEqual(test1.shortcut, "title-00002")

        test2b = self.env[self.model_2b.model].create(
            {"name": "Test Group", "share": False}
        )
        self.assertEqual(test2b.comment, "False-00001")
        test2b.comment = ""
        self.assertEqual(test2b.comment, "")
        test2b.sequence_code_set()
        self.assertEqual(test2b.comment, "False-00002")

        title = self.env.ref("base.res_partner_title_madam")
        test2m = self.env[self.model_2m.model].create(
            {"name": "Test Contact", "title": title.id}
        )
        self.assertEqual(test2m.ref, f"{title.id}-00001")
        test2m.ref = ""
        self.assertEqual(test2m.ref, "")
        test2m.sequence_code_set()
        self.assertEqual(test2m.ref, f"{title.id}-00002")

    def test_3_sequence_2s(self):
        self.model_2s = self.env.ref("base.model_res_lang")
        # Count sequences
        Sequence = self.env["ir.sequence"]
        count1 = Sequence.search_count([])
        self.model_2s.sequence_code_field_id = self._get_field(self.model_2s.id, "iso_code").id
        count2 = Sequence.search_count([])
        self.assertEqual(count1 + 1, count2)
        self.model_2s.sequence_selection_field_id = self._get_field(self.model_2s.id, "direction").id
        count3 = Sequence.search_count([])
        self.assertEqual(count2 + 2, count3)
        self.model_2s.sequence_selection_field_id = False
        count4 = Sequence.search_count([])
        self.assertEqual(count3, count4)
        self.model_2s.sequence_selection_field_id = self._get_field(self.model_2s.id, "direction").id
        count5 = Sequence.search_count([])
        self.assertEqual(count4, count5)
        # Regular tests
        test2s = self.env[self.model_2s.model].create(
            {"name": "Test Language", "direction": "ltr", "code": "test"}
        )
        self.assertEqual(test2s.iso_code, "ltr-00001")
        test2s.iso_code = ""
        self.assertEqual(test2s.iso_code, "")
        test2s.sequence_code_set()
        self.assertEqual(test2s.iso_code, "ltr-00002")
