import frappe
from frappe.tests.utils import FrappeTestCase


class TestTaskSubtaskDepth(FrappeTestCase):
	def test_one_level_subtask_allowed(self):
		parent = frappe.get_doc(
			{"doctype": "Task", "subject": "Parent Task", "is_group": 1}
		).insert()
		child = frappe.get_doc(
			{
				"doctype": "Task",
				"subject": "Child Task",
				"parent_task": parent.name,
			}
		).insert()

		self.assertEqual(child.parent_task, parent.name)

	def test_second_level_subtask_rejected(self):
		parent = frappe.get_doc(
			{"doctype": "Task", "subject": "Parent Task 2", "is_group": 1}
		).insert()
		child = frappe.get_doc(
			{
				"doctype": "Task",
				"subject": "Child Task 2",
				"is_group": 1,
				"parent_task": parent.name,
			}
		).insert()

		grandchild = frappe.get_doc(
			{
				"doctype": "Task",
				"subject": "Grandchild Task 2",
				"parent_task": child.name,
			}
		)

		self.assertRaises(frappe.ValidationError, grandchild.insert)
