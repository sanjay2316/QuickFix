# Copyright (c) 2026, Sanjay and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		settings = frappe.get_doc('QuickFix Settings')
		self.labour_charge = settings.default_labour_charge
		self.final_amount = self.labour_charge + self.parts_total

	def before_save(self):
		for row in self.parts_used:
			itemq = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			if itemq < row.quantity :
					frappe.throw( f"Unavaible of Stock {row.part} Stock left : {itemq}")

	def on_submit(self):
		for row in self.parts_used:
			itemq = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			frappe.db.set_value("Spare Part",row.part,"stock_qty",itemq-row.quantity)
			newdoc = frappe.new_doc("Service Invoice")
			newdoc.job_card = self.name
			newdoc.save()
			frappe.enqueue("quickfix.api.send_mail",queue="default",name=self.customer,total=self.final_amount)
	def on_cancel(self):
		self.status = "Cancle"
		for row in self.parts_used:
			itemq = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			frappe.db.set_value("Spare Part",row.part,"stock_qty",itemq+row.quantity)
	def on_trash(self):
		if self.status != "Draft" or self.status != "Cancelled" :
			frappe.throw("Cannot be Deleted ! ")
				
	
						



