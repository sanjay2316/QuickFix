import frappe
from frappe.model.workflow import apply_workflow
from frappe.query_builder import DocType
from frappe.utils import today,add_days

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

@frappe.whitelist()
def get_overdue_jobs():
    jobs = DocType("Job Card")
    seventh_day = add_days(today(),-7)
    result = (
        frappe.qb.from_(jobs).select(jobs.name, jobs.customer_name, jobs.assigned_technician,jobs.creation).where(jobs.status.isin(["Pending Diagnosis", "In Repair"]) and (jobs.creation<seventh_day)).run(as_dict=True)
    )
    return result
#http://127.0.0.1:8001/api/method/quickfix.api.get_overdue_jobs

@frappe.whitelist()
def transfer_job(from_tech,to_tech):
    try :
        frappe.db.sql("""
            update `tabJob Card` j set j.assigned_technician = %s where j.assigned_technician = %s
        """,(to_tech,from_tech))
        frappe.db.commit()
    except Exception :
        print("Error")
#http://127.0.0.1:8001/api/method/quickfix.api.transfer_job?from_tech=TECH-0001&to_tech=TECH-0002

@frappe.whitelist()
def check_low_stock():
    lowq = frappe.db.sql(""" select s.part_name from `tabSpare Part` where stock_qty < 10
    """)
    for low in lowq:
        print(low)
    return