import frappe
from frappe.model.workflow import apply_workflow


@frappe.whitelist()
def approve_job(name):
    print("hi")
    doc = frappe.get_doc("Job Card", name)
    if doc.workflow_state != "Awaiting Customer Approval":
        frappe.throw(
            f"Job Card {doc.name} is not in Pending Approval state."
        )
    apply_workflow(doc, "Approve")
    doc.status = "In Repair"
    doc.save()
    return {
        "name": doc.name,
        "status": doc.status,
        "workflow_state": doc.workflow_state
    }
