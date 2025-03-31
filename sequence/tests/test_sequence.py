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
        model = self.env.ref("base.model_res_lang")
        record = self.env[model.model].create({"name": "Test Lang", "code": "test"})
        self.assertEqual(record.name, "Test Lang")

    def test_1_action(self):
        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        action = self.env["ir.actions.server"].search(
            [
                ("model_id", "=", model.id),
                ("binding_model_id", "=", model.id),
                ("usage", "=", "ir_actions_server"),
                ("state", "=", "code"),
                ("code", "=", "for rec in records:\n  rec.set_sequence_code()"),
            ]
        )
        self.assertTrue(action)

    def test_1_secuence(self):
        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        record = self.env[model.model].create({"name": "Test Lang", "code": "test"})
        self.assertEqual(record.iso_code, "lang-00001")
        record.iso_code = ""
        self.assertEqual(record.iso_code, "")
        record.set_sequence_code()
        self.assertEqual(record.iso_code, "lang-00002")

    def test_count_sequences_and_actions(self):
        Sequence = self.env["ir.sequence"]
        Action = self.env["ir.actions.server"]
        seq_count1 = Sequence.search_count([])
        act_count1 = Action.search_count([])

        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        seq_count2 = Sequence.search_count([])
        act_count2 = Action.search_count([])
        self.assertEqual(seq_count1 + 1, seq_count2)
        self.assertEqual(act_count1 + 1, act_count2)

        model.sequence_code_field_id = False
        seq_count3 = Sequence.search_count([])
        act_count3 = Action.search_count([])
        self.assertEqual(seq_count2, seq_count3)
        self.assertEqual(act_count2, act_count3)

        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        seq_count4 = Sequence.search_count([])
        act_count4 = Action.search_count([])
        error_message = "{} should exist already and not be created again."
        self.assertEqual(seq_count3, seq_count4, error_message.format("Sequence"))
        self.assertEqual(act_count3, act_count4, error_message.format("Action"))

    def test_no_change_of_existing_sequence_code(self):
        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        record = self.env[model.model].create({"name": "Test Lang", "code": "test"})
        self.assertEqual(record.iso_code, "lang-00001")
        record.set_sequence_code()
        self.assertEqual(record.iso_code, "lang-00001")

    def test_no_name_get_next_sequence_code(self):
        model = self.env.ref("base.model_res_partner")
        model.sequence_code_field_id = self._get_field(model.id, "ref").id
        record = self.env[model.model].create({"type": "other"})
        self.assertEqual(record.name, "partner-00001")

    # TODO: test sequence.mixin
