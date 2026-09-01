import frappe


def validate_subtask_depth(doc, method=None):
	"""Subtasks are capped at one level: a task that is already a subtask
	cannot itself become a parent of another subtask."""
	if not doc.parent_task:
		return

	parent_is_itself_a_subtask = frappe.db.get_value("Task", doc.parent_task, "parent_task")
	if parent_is_itself_a_subtask:
		frappe.throw(
			frappe._(
				"Subtasks are limited to one level. {0} is already a subtask and cannot have further subtasks."
			).format(doc.parent_task)
		)
