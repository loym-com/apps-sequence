import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestSequence(TransactionCase):

    @classmethod
    def _get_field(cls, model_id, field_name):
        return cls.env["ir.model.fields"].search(
            [("model_id", "=", model_id), ("name", "=", field_name)]
        ).ensure_one()

    def test_choice_boolean(self):
        model = self.env.ref("base.model_res_groups")
        model.sequence_code_field_id = self._get_field(model.id, "comment").id
        model.sequence_choice_field_id = self._get_field(model.id, "share").id
        record = self.env[model.model].create(
            {"name": "Test Group", "share": False}
        )
        self.assertEqual(record.comment, "False-00001")
        record.comment = ""
        self.assertEqual(record.comment, "")
        record.set_sequence_code()
        self.assertEqual(record.comment, "False-00002")

    # def test_choice_many2one(self):
    #     model = self.env.ref("base.model_res_partner")
    #     model.sequence_code_field_id = self._get_field(model.id, "ref").id
    #     model.sequence_choice_field_id = self._get_field(model.id, "title").id
    #     title = self.env.ref("base.res_partner_title_madam")
    #     record = self.env[model.model].create(
    #         {"name": "Test Contact", "title": title.id}
    #     )
    #     self.assertEqual(record.ref, f"{title.id}-00001")
    #     record.ref = ""
    #     self.assertEqual(record.ref, "")
    #     record.set_sequence_code()
    #     self.assertEqual(record.ref, f"{title.id}-00002")

    def test_choice_selection(self):
        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        model.sequence_choice_field_id = self._get_field(model.id, "direction").id
        record = self.env[model.model].create(
            {"name": "Test Language", "direction": "ltr", "code": "test"}
        )
        self.assertEqual(record.iso_code, "ltr-00001")
        record.iso_code = ""
        self.assertEqual(record.iso_code, "")
        record.set_sequence_code()
        self.assertEqual(record.iso_code, "ltr-00002")

    def test_count_sequences(self):
        Sequence = self.env["ir.sequence"]
        model = self.env.ref("base.model_res_lang")
        model.sequence_code_field_id = self._get_field(model.id, "iso_code").id
        seq_count1 = Sequence.search_count([])
        model.sequence_choice_field_id = self._get_field(model.id, "direction").id
        seq_count2 = Sequence.search_count([])
        self.assertEqual(seq_count1 + 2, seq_count2, "Add 2 directions: ltr and rtl")
