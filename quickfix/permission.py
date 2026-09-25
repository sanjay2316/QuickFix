import frappe


def jobcard_query(user=None):
	if not user:
		user = frappe.session.user
	user = frappe.db.escape(user)
	if user in "Technician":
		return f"""
            tabJob Card.name IN (
                SELECT parent
                FROM tabJob Card Technician
                WHERE user = {user}
            )"""
