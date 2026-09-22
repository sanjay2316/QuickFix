import frappe
def jobcard_query(user):
    if not user:
        user = frappe.session.user
    return "(`tabToDo`.owner = {user} or `tabToDo`.assigned_by = {user})".format(user=frappe.db.escape(user))
