# Copyright (c) 2026, Sanjay and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: None):
	columns = get_columns()
	data = get_data()
	graph = get_graph(data)
	return columns, data, None, graph


def get_columns():
	return [
		{
			"label": _("Technician Name"),
			"fieldname": "technician_name",
			"fieldtype": "Data",
		},
		{
			"label": _("Total Jobs"),
			"fieldname": "total_jobs",
			"fieldtype": "Int",
		},
		{
			"label": _("Completed Jobs"),
			"fieldname": "completed_jobs",
			"fieldtype": "Int",
		},
		{
			"label": _("Revenue"),
			"fieldname": "revenue",
			"fieldtype": "Currency",
		},
		{
			"label": _("Completion Rate"),
			"fieldname": "completion_rate",
			"fieldtype": "Float",
		},
	]


def get_data():
	res = frappe.db.sql(
		"""
		select
		j.assigned_technician as technician_name,
		count(*) as total_jobs,
		sum(Case when j.status='Ready for Delivery' or j.status='Delivered' then 1 else 0 end) as completed_jobs,
		sum(j.final_amount) as revenue,
		sum(Case When j.status='Ready for Delivery' or j.status='Delivered' then 1 else 0 end)/(count(*))*100 as completion_rate
		from `tabJob Card` j
		where j.status != 'Rejected'
		group by j.assigned_technician
	""",
		as_dict=True,
	)
	return res


def get_graph(data):
	if not data:
		return None
	labels = [row.technician_name for row in data]
	total = [int(row.total_jobs or 0) for row in data]
	completed = [int(row.completed_jobs or 0) for row in data]
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Total Jobs", "values": total},
				{"name": "Completed Jobs", "values": completed},
			],
		},
		"type": "bar",
		"height": 300,
		"colors": ["#000000", "#FF0000"],
	}
