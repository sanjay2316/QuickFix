// // Copyright (c) 2026, Sanjay and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Spare Part", {
	validate(frm) {
        if(frm.doc.selling_cost <= frm.doc.unit_cost){
            frappe.throw("Selling Price should be Greater than Unit Cost !");
        }
	},
});
