# Copyright (c) 2026, Sanjay and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries


class SparePart(Document):
	def autoname(self):
		if self.is_active:
			self.name = self.part_code.upper()
		else:
			series = getseries("PART-2026", 9)
			self.name = f"{'PART-2026'}-{series}"
