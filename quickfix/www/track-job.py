import frappe

def get_context(context):
    job = frappe.db.get_list("Job Card")
    context["joblist"] = job