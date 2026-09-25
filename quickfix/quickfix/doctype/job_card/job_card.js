// Copyright (c) 2026, Sanjay and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	setup(frm) {
		Assigned_technician_filter(frm);
	},
	device_type(frm) {
		Assigned_technician_filter(frm);
	},
	refresh(frm) {
		frm.add_custom_button("Reject Job", () => {
			let d = new frappe.ui.Dialog({
				title: "Reject the Job",
				fields: [
					{
						label: "Rejection Reason",
						fieldname: "rejection_reason",
						fieldtype: "Small Text",
						reqd: 1,
					},
				],
				primary_action_label: "Reject Job",
				primary_action(values) {
					frm.set_value("status", "Cancelled");
					frm.set_value("workflow_state", "Rejected");
					frm.save();
					console.log(values);
					d.hide();
				},
			});
			d.show();
		}),
			frm.add_custom_button("Transfer Technician", () => {
				frappe.prompt(
					[
						{
							label: "Assigned Technician",
							fieldname: "assigned_technician",
							fieldtype: "Link",
							options: "Technician",
							reqd: 1,
						},
					],
					(values) => {
						frappe.confirm(
							"Are you sure you want to change the technician",
							async () => {
								frm.set_value("assigned_technician", values.assigned_technician);
								frm.save();
								frm.trigger("assigned_technician");
								await frappe.call({
									method: "quickfix.api.success_msg",
									args: {
										name: frm.name,
									},
								});
							},
							() => {}
						);
					}
				);
			});
	},
	async assigned_technician(frm) {
		let spec = frappe.db.get_value(
			"Technician",
			frm.doc.assigned_technician,
			"specialization"
		);
		console.log("Hello");
		if (frm.doc.device_type != spec) {
			await frappe.msgprint("device_type and specialization mismatched", "Alert Msg");
		}
	},
	validate(frm) {
		if (
			frm.doc.status != "Draft" &&
			frm.doc.status != "Pending Diagonsis" &&
			frm.doc.assigned_technician === ""
		) {
			frappe.throw("Assigned_technician must exist if status is In Repair or beyond !");
		}
		let sum = 0;
		frm.doc.parts_used.forEach((row) => {
			row.total_price = row.unit_price * row.quantity;
			sum = sum + row.total_price;
		});
		frm.set_value("parts_total", sum);
	},
	before_submit(frm) {
		if (frm.doc.status != "Ready for Delivery") {
			frappe.throw("Submission Failed ! (Reason -> current status cannot be submitted)");
		}
	},
});

function Assigned_technician_filter(frm) {
	frm.set_query("assigned_technician", () => {
		return {
			filters: {
				specialization: frm.doc.device_type,
				status: "Active",
			},
		};
	});
}
