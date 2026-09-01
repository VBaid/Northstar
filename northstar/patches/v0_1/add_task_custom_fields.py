from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Task": [
				{
					"fieldname": "custom_source_type",
					"label": "Source Type",
					"fieldtype": "Select",
					"options": "Manual\nMOM\nWorkflow\nRecurring",
					"default": "Manual",
					"insert_after": "type",
				},
				{
					"fieldname": "custom_mom",
					"label": "MOM",
					"fieldtype": "Link",
					"options": "MOM",
					"insert_after": "custom_source_type",
					"read_only": 1,
					"depends_on": "eval:doc.custom_source_type=='MOM'",
				},
				{
					"fieldname": "custom_mom_item",
					"label": "MOM Item",
					"fieldtype": "Data",
					"insert_after": "custom_mom",
					"read_only": 1,
					"hidden": 1,
				},
			]
		}
	)
