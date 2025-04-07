import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestProjectDisplay(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_model = cls.env.ref("project.model_project_project")
        cls.project_model.display_code_pattern = ""
        cls.project = cls.env["project.project"].create({"name": "Test Project"})

    def test_1_empty_display_code(self):
        self.assertEqual(self.project.display_code, False)
    
    def test_compute_display_code(self):
        # Empty
        self.project_model.display_code_pattern = "{name}"
        self.project.name = "Name"
        self.assertEqual(self.project.display_code, "Name")
        # Not empty
        self.project.name = "NEW NAME"
        # self.project._invalidate_cache(["display_code"])
        self.assertEqual(self.project.display_code, "Name")

    def test_inverse_display_code(self):
        self.project.display_code = "custom"
        self.assertEqual(self.project.display_code, "custom")

    def test_method_set_missing_stored_display_code(self):
        self.project_model.display_code_pattern = "{name}"
        # Empty
        self.project_model.set_missing_stored_display_code()
        self.assertEqual(self.project.display_code, "Test Project")
        # Not empty
        self.project.display_code = "P001"
        # self.project._invalidate_cache(["display_code"])
        self.project_model.set_missing_stored_display_code()
        self.assertEqual(self.project.display_code, "P001")
