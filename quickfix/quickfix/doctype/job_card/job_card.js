// Copyright (c) 2026, Sanjay and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
    setup(frm){
        Assigned_technician_filter(frm)
    },
    device_type(frm){
        Assigned_technician_filter(frm)
    },
	validate(frm) {
        if(frm.doc.status != "Draft" && frm.doc.status != "Pending Diagonsis" && frm.doc.assigned_technician === ""){
            frappe.throw("Assigned_technician must exist if status is In Repair or beyond !")
        }
        let sum = 0
        frm.doc.parts_used.forEach(row => {
            row.total_price = (row.unit_price*row.quantity)
            sum=sum+row.total_price;
        });
        frm.set_value("parts_total",sum)
	},
    before_submit(frm){
        if(frm.doc.status!="Ready for Delivery"){
            frappe.throw("Submission Failed ! (Reason -> current status cannot be submitted)")
        }
    },
});


function Assigned_technician_filter(frm){
    frm.set_query("assigned_technician", () => {
            return {
                filters: {
                    specialization: frm.doc.device_type
                }
            }
        })
}