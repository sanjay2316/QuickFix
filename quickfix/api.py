import frappe
def send_mail(name,total):
    emailid = frappe.db.get_value("Customers",name,"email")
    frappe.sendmail(recipients=[emailid],subject="QuickFix Invoice",message=f"invoice amount {total}")
