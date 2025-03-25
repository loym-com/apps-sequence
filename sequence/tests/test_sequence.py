"""
Test data:
- ir.model record - ir.attachment (name)
+ ir.model record with sequence_code_field_id - res.partner.title (shortcut)
+ ir.model record with sequence_code_field_id and sequence_selection_field_id (boolean) - res.groups (comment/share)
- ir.model record with sequence_code_field_id and sequence_selection_field_id (many2one) - res.partner.bank (acc_number/bank_id)
- ir.model record with sequence_code_field_id and sequence_selection_field_id (selection) - res.partner(ref/company_type)
Tests to do with the test data:
- self.create()
- record.write(delete sequence code)
- record.sequence_code_set()

TODO: count ir.sequence
"""

from odoo.tests.common import TransactionCase


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
        cls.model_1.sequence_code_field_id = cls._get_field(cls.model_1.id, "shortcut").id  # res.country.state? name,code
        # code, boolean
        cls.model_2b = cls.env.ref("base.model_res_groups")
        cls.model_2b.sequence_code_field_id = cls._get_field(cls.model_2.id, "comment").id
        cls.model_2b.sequence_selection_field_id = cls._get_field(cls.model_2.id, "share").id
        # code, manyone
        cls.model_2m = cls.env.ref("base.model_res_partner")
        cls.model_2m.sequence_code_field_id = cls._get_field(cls.model_2.id, "ref").id
        cls.model_2m.sequence_selection_field_id = cls._get_field(cls.model_2.id, "title").id
        # # code, selection
        # cls.model_2s = cls.env.ref("base.model_res_lang")
        # cls.model_2s.sequence_code_field_id = cls._get_field(cls.model_2.id, "iso_code").id
        # cls.model_2s.sequence_selection_field_id = cls._get_field(cls.model_2.id, "direction").id

    def setUp(self):
        super().setUp()

    def tests(self):
        action = self.env["ir.actions.server"].search(
            [
                ("model_id", "=", self.model_1.id),
                ("binding_model_id", "=", self.model_1.id),
                ("usage", "=", "ir_actions_server"),
                ("state", "=", "code"),
                ("name", "=", "Set Sequence"),
            ]
        )
        self.AssertTrue(action)

        # code, selection
        Sequence = self.env["ir.sequence"]
        self.model_2s = self.env.ref("base.model_res_lang")
        count1 = Sequence.search_count([])
        self.model_2s.sequence_code_field_id = self._get_field(self.model_2.id, "iso_code").id
        count2 = Sequence.search_count([])
        self.assertEqual(count1 + 1, count2)
        self.model_2s.sequence_selection_field_id = self._get_field(self.model_2.id, "direction").id
        count3 = Sequence.search_count([])
        self.assertEqual(count2 + 2, count3)
        self.model_2s.sequence_selection_field_id = False
        count4 = Sequence.search_count([])
        self.assertEqual(count3, count4)
        self.model_2s.sequence_selection_field_id = self._get_field(self.model_2.id, "direction").id
        count5 = Sequence.search_count([])
        self.assertEqual(count4, count5)


        test0 = self.env[self.model_0._name].create({"name": "Test Attachment"})
        self.assertEqual(test0.name, "Test Attachment")

        test1 = self.env[self.model_1._name].create({"name": "Test Partner Title"})
        self.assertEqual(test1.shortcut, "title-00001")
        test1.shortcut = ""
        self.assertEqual(test1.shortcut, "")
        test1.sequence_code_set()
        self.assertEqual(test1.shortcut, "title-00002")

        test2b = self.env[self.model_2b._name].create(
            {"name": "Test Group", "share": False}
        )
        self.assertEqual(test2b.comment, "False-00001")
        test2b.comment = ""
        self.assertEqual(test2b.comment, "")
        test2b.sequence_code_set()
        self.assertEqual(test2b.comment, "False-00002")

        title = self.env.ref("base.res_partner_title_madam")
        test2m = self.env[self.model_2m._name].create(
            {"name": "Test Contact", "title": title.id}
        )
        self.assertEqual(test2m.ref, f"{title.id}-00001")
        test2m.comment = ""
        self.assertEqual(test2m.ref, "")
        test2m.sequence_code_set()
        self.assertEqual(test2m.ref, f"{title.id}-00002")

        test2s = self.env[self.model_2s._name].create(
            {"name": "Test Language", "direction": "ltr", "code": "test"}
        )
        self.assertEqual(test2s.iso_code, "ltr-00001")
        test2s.comment = ""
        self.assertEqual(test2s.iso_code, "")
        test2s.sequence_code_set()
        self.assertEqual(test2s.iso_code, "ltr-00002")
