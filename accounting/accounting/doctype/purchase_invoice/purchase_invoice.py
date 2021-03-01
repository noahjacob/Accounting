# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry

class PurchaseInvoice(Document):
	def before_save(self):
		self.total_amount,self.total_quantity = 0,0
		if not self.items:
			frappe.throw("Add some Items before saving")
		for d in self.items:
			self.total_quantity = flt(self.total_quantity) + flt(d.item_quantity)
			self.total_amount = flt(self.total_amount) + flt(d.amount)
	
	def on_submit(self):
		default_payable_account = frappe.get_value('Company',self.company,'default_payable_account')
		stock_received_but_not_billed = frappe.get_value('Company',self.company,'stock_received_but_not_billed')
		make_gl_entry(self,stock_received_but_not_billed,self.total_amount,flt(0))
		make_gl_entry(self,default_payable_account,flt(0),self.total_amount)
	def on_cancel(self):
		# cancel gl entry
		make_reverse_gl_entry(self,self.doctype,self.name)
		


@frappe.whitelist()
def get_purchase_receipt_items(name=None):
	parent = frappe.get_doc('Purchase Receipt',name)
	return parent.items