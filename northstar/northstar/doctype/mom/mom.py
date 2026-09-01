import frappe
from frappe.model.document import Document


class MOM(Document):
	def on_update(self):
		self.create_tasks_for_action_items()

	def create_tasks_for_action_items(self):
		"""Auto-convert Action items with no linked task yet into Tasks."""
		for item in self.items:
			if item.item_type != "Action" or item.task:
				continue

			task = frappe.new_doc("Task")
			task.subject = item.description
			task.project = self.project
			task.company = self.company
			task.exp_end_date = item.due_date
			task.custom_source_type = "MOM"
			task.custom_mom = self.name
			task.custom_mom_item = item.name
			task.insert(ignore_permissions=True)

			frappe.db.set_value("MOM Item", item.name, "task", task.name)
			item.task = task.name

			if item.item_owner:
				from frappe.desk.form.assign_to import add as assign_to_add

				assign_to_add(
					{
						"doctype": "Task",
						"name": task.name,
						"assign_to": [item.item_owner],
					}
				)
