import frappe
from frappe.tests.utils import FrappeTestCase


def get_test_company():
	company = frappe.db.get_default("Company")
	if company:
		return company
	return frappe.get_all("Company", limit=1, pluck="name")[0]


class TestMOM(FrappeTestCase):
	def setUp(self):
		if not frappe.db.exists("Meeting Type", "Weekly Ops Review"):
			frappe.get_doc(
				{
					"doctype": "Meeting Type",
					"meeting_type_name": "Weekly Ops Review",
				}
			).insert()

	def test_action_item_creates_task_but_decision_does_not(self):
		company = get_test_company()

		mom = frappe.get_doc(
			{
				"doctype": "MOM",
				"meeting_type": "Weekly Ops Review",
				"title": "Test Ops Review",
				"held_on": frappe.utils.now_datetime(),
				"chair": "Administrator",
				"company": company,
				"items": [
					{
						"item_type": "Action",
						"description": "Follow up with vendor on pricing",
						"item_owner": "Administrator",
					},
					{
						"item_type": "Decision",
						"description": "Approved the new budget",
					},
				],
			}
		).insert()
		mom.reload()

		action_item = mom.items[0]
		decision_item = mom.items[1]

		self.assertTrue(action_item.task, "Action item should have an auto-created task")
		self.assertFalse(decision_item.task, "Decision item should not create a task")

		task = frappe.get_doc("Task", action_item.task)
		self.assertEqual(task.subject, "Follow up with vendor on pricing")
		self.assertEqual(task.custom_source_type, "MOM")
		self.assertEqual(task.custom_mom, mom.name)
		self.assertEqual(task.custom_mom_item, action_item.name)

	def test_saving_again_does_not_duplicate_task(self):
		company = get_test_company()

		mom = frappe.get_doc(
			{
				"doctype": "MOM",
				"meeting_type": "Weekly Ops Review",
				"title": "Test Ops Review 2",
				"held_on": frappe.utils.now_datetime(),
				"chair": "Administrator",
				"company": company,
				"items": [
					{"item_type": "Action", "description": "Draft the contract"},
				],
			}
		).insert()
		mom.reload()

		first_task = mom.items[0].task
		self.assertTrue(first_task)

		mom.minutes_text = "Updated minutes"
		mom.save()
		mom.reload()

		self.assertEqual(mom.items[0].task, first_task)
		self.assertEqual(
			frappe.db.count("Task", {"custom_mom_item": mom.items[0].name}),
			1,
		)
