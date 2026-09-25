import frappe
from frappe.utils import now, today


@frappe.whitelist()
def log_change(doc, method=None):
	if doc.doctype == "Audit Log":
		return
	doc1 = frappe.new_doc("Audit Log")
	doc1.doctype_name = doc.doctype
	doc1.document_name = doc.name
	doc1.action = method
	doc1.user = frappe.session.user
	doc1.time = now
	doc1.insert()
	frappe.db.commit()
