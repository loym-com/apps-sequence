# Copyright 2016 Tecnativa <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.tests.common as common


class TestProjectTask(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.task_model = self.env["project.task"]
        self.ir_sequence_model = self.env["ir.sequence"]
        self.task_sequence = self.env["ir.sequence"].search(
            [("code", "=", "project.task")]
        )

    def test_old_task_sequence_code_assign(self):
        tasks = self.task_model.search([])
        for task in tasks:
            self.assertNotEqual(task.sequence_code, "/")

    def test_new_task_sequence_code_assign(self):
        number_next = self.task_sequence.number_next_actual
        sequence_code = self.task_sequence.get_next_char(number_next)
        task = self.task_model.create(
            {
                "name": "Testing task sequence_code",
            }
        )
        self.assertNotEqual(task.sequence_code, "/")
        self.assertEqual(task.sequence_code, sequence_code)

    def test_name_get(self):
        number_next = self.task_sequence.number_next_actual
        sequence_code = self.task_sequence.get_next_char(number_next)
        task = self.task_model.create(
            {
                "name": "Task Testing Get Name",
            }
        )
        result = task.display_name
        self.assertEqual(result, f"[{sequence_code}] Task Testing Get Name")

    def test_name_search(self):
        task = self.env["project.task"].create(
            {"name": "Such Much Task", "sequence_code": "TEST-123"}
        )

        result = task.name_search("TEST-123")
        self.assertIn(
            task.id,
            map(lambda x: x[0], result),
            f"Task with sequence_code {task.sequence_code} should be in the results",
        )

        result = task.name_search("TEST")
        self.assertIn(
            task.id,
            map(lambda x: x[0], result),
            f"Task with sequence_code {task.sequence_code} should be in the results",
        )

        result = task.name_search("much")
        self.assertIn(
            task.id,
            map(lambda x: x[0], result),
            f"Task with sequence_code {task.sequence_code} should be in the results",
        )

        result = task.name_search("20232")
        self.assertNotIn(
            task.id,
            map(lambda x: x[0], result),
            f"Task with sequence_code {task.sequence_code} shouldn't be in the results",
        )
