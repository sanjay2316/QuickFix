import frappe


def get_name():
	doc = frappe.db.get_single_value("QuickFix Settings", "shop_name")
	return doc
