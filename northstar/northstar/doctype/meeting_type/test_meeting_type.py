import frappe
from frappe.tests.utils import FrappeTestCase


class TestMeetingType(FrappeTestCase):
	def test_create_meeting_type(self):
		if frappe.db.exists("Meeting Type", "Weekly Ops Review"):
			frappe.delete_doc("Meeting Type", "Weekly Ops Review", force=True)

		doc = frappe.get_doc(
			{
				"doctype": "Meeting Type",
				"meeting_type_name": "Weekly Ops Review",
			}
		).insert()

		self.assertEqual(doc.name, "Weekly Ops Review")
		self.assertEqual(doc.is_active, 1)
