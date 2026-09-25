// Copyright (c) 2026, Sanjay and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customers", {
	refresh(frm) {},
	validate(frm) {
		if (frm.doc.phone.length < 10) {
			frappe.throw("Invalid Phone ! (Reason -> 10 digit required)");
		}
	},
});
