# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry

class PurchaseReceipt(Document):
	def before_save(self):
		self.total_amount,self.total_quantity = 0,0
		if not self.items:
			frappe.throw("Add some Items before saving")
		for d in self.items:
			self.total_quantity = flt(self.total_quantity) + flt(d.item_quantity)
			self.total_amount = flt(self.total_amount) + flt(d.amount)

	def on_submit(self):
		default_inventory_account = frappe.get_value('Company',self.company,'default_inventory_account')
		
		make_gl_entry(self,default_inventory_account,self.total_amount,flt(0))
		make_gl_entry(self,'Stock Received But Not Billed - S',flt(0),self.total_amount)


@frappe.whitelist()
def get_purchase_order_items(name=None):
	parent = frappe.get_doc('Purchase Order',name)
	return parent.items


