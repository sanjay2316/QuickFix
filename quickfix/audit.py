import frappe
from frappe.utils import now, today


@frappe.whitelist()
def log_change(doctype, name):
	doc = frappe.new_doc("Audit Log")
	doc.doctype_name = doctype
	doc.document_name = name
	doc.action = "method"
	doc.user = frappe.session.user
	doc.time = now
	doc.insert()
	frappe.db.commit()
