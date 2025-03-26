import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestSequence(TransactionCase):

    @classmethod
    def _get_field(cls, model_id, field_name):
        return cls.env["ir.model.fields"].search(
            [("model_id", "=", model_id), ("name", "=", field_name)]
        ).ensure_one()

    def test_0_sequence(self):
        model = self.env.ref("base.model_ir_attachment")
        record = self.env[model.model].create({"name": "Test Attachment"})
        self.assertEqual(record.name, "Test Attachment")

    def test_1_action(self):
        model = self.env.ref("base.model_res_partner_title")
        model.sequence_code_field_id = self._get_field(model.id, "shortcut").id
        action = self.env["ir.actions.server"].search(
            [
                ("model_id", "=", model.id),
                ("binding_model_id", "=", model.id),
                ("usage", "=", "ir_actions_server"),
                ("state", "=", "code"),
                ("code", "=", "for rec in records:\n  rec.sequence_code_set()"),
            ]
        )
        self.assertTrue(action)

    def test_1_secuence(self):
        model = self.env.ref("base.model_res_partner_title")
        model.sequence_code_field_id = self._get_field(model.id, "shortcut").id
        record = self.env[model.model].create({"name": "Test Partner Title"})
        self.assertEqual(record.shortcut, "title-00001")
        record.shortcut = ""
        self.assertEqual(record.shortcut, "")
        record.sequence_code_set()
        self.assertEqual(record.shortcut, "title-00002")

    def test_2_multi_boolean(self):
        model = self.env.ref("base.model_res_groups")
        model.sequence_code_field_id = self._get_field(model.id, "comment").id
        model.sequence_selection_field_id = self._get_field(model.id, "share").id
        record = self.env[model.model].create(
            {"name": "Test Group", "share": False}
        )
        self.assertEqual(record.comment, "False-00001")
        record.comment = ""
        self.assertEqual(record.comment, "")
        record.sequence_code_set()
        self.assertEqual(record.comment, "False-00002")

    def test_2_multi_many2one(self):
        model = self.env.ref("base.model_res_partner")
        model.sequence_code_field_id = self._get_field(model.id, "ref").id
        model.sequence_selection_field_id = self._get_field(model.id, "title").id
        title = self.env.ref("base.res_partner_title_madam")
        record = self.env[model.model].create(
            {"name": "Test Contact", "title": title.id}
        )
        self.assertEqual(record.ref, f"{title.id}-00001")
        record.ref = ""
        self.assertEqual(record.ref, "")
        record.sequence_code_set()
        self.assertEqual(record.ref, f"{title.id}-00002")

    def test_2_multi_selection(self):
        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        model.sequence_selection_field_id = self._get_field(model.id, "direction").id
        record = self.env[model.model].create(
            {"name": "Test Language", "direction": "ltr", "code": "test"}
        )
        self.assertEqual(record.iso_code, "ltr-00001")
        record.iso_code = ""
        self.assertEqual(record.iso_code, "")
        record.sequence_code_set()
        self.assertEqual(record.iso_code, "ltr-00002")

    def test_count_sequences_and_actions(self):
        Sequence = self.env["ir.sequence"]
        Action = self.env["ir.actions.server"]
        seq_count1 = Sequence.search_count([])
        act_count1 = Action.search_count([])
        # test_2_multi_selection with counting
        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        seq_count2 = Sequence.search_count([])
        act_count2 = Action.search_count([])
        self.assertEqual(seq_count1 + 1, seq_count2)
        self.assertEqual(act_count1 + 1, act_count2)
        model.sequence_code_field_id = False
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        act_count3 = Action.search_count([])
        self.assertEqual(act_count2, act_count3, "Action should exist already and not be created again.")
        model.sequence_selection_field_id = self._get_field(model.id, "direction").id
        seq_count3 = Sequence.search_count([])
        self.assertEqual(seq_count2 + 2, seq_count3)
        model.sequence_selection_field_id = False
        seq_count4 = Sequence.search_count([])
        self.assertEqual(seq_count3, seq_count4)
        model.sequence_selection_field_id = self._get_field(model.id, "direction").id
        seq_count5 = Sequence.search_count([])
        self.assertEqual(seq_count4, seq_count5, "Sequences should exist already and not be created again.")

    def test_no_change_of_existing_sequence_code(self):
        # test_2_multi_selection copy
        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        model.sequence_selection_field_id = self._get_field(model.id, "direction").id
        record = self.env[model.model].create(
            {"name": "Test Language", "direction": "ltr", "code": "test"}
        )
        self.assertEqual(record.iso_code, "ltr-00001")
        # New test
        record.sequence_code_set()
        self.assertEqual(record.iso_code, "ltr-00001")

    def test_no_name_get_sequence_code(self):
        # test_2_multi_many2one copy
        model = self.env.ref("base.model_res_partner")
        model.sequence_code_field_id = self._get_field(model.id, "ref").id
        model.sequence_selection_field_id = self._get_field(model.id, "title").id
        title = self.env.ref("base.res_partner_title_madam")
        # No name
        record = self.env[model.model].create(
            {"type": "other", "title": title.id}
        )
        self.assertEqual(record.name, f"{title.id}-00001")

    # TODO: test sequence.mixin
