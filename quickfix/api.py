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

@frappe.whitelist()
def create_device_type():
    doc1 = frappe.get_doc("Device Type","Device1")
    doc1.device_type("Device1")
    doc1.insert()
    doc2 = frappe.get_doc("Device Type","Device2")
    doc2.device_type("Device2")
    doc2.insert()
    doc3 = frappe.get_doc("Device Type","Device3")
    doc3.device_type("Device3")
    doc3.insert()
    settings = frappe.get_doc("QuickFix Settings")
    settings.manager_email = "manager1@quickfix.com"
    settings.save()

@frappe.whitelist()
def success_msg():
    frappe.msgprint(
        msg ='Technician Changed Succesfully',
        title = 'Success_msg',
        indicator = 'green',
    )
    return 

@frappe.whitelist()
def get_job_summary(job_card_name):
    doc = frappe.db.get("Job Card",job_card_name)
    return doc.device_type
#http://127.0.0.1:8001/api/method/quickfix.api.get_job_summary?job_card_name=JC-2026-00002