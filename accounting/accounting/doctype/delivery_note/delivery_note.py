# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt


class DeliveryNote(Document):
	def validate(self):
		self.total_amount, self.total_quantity, self.total_cost_price = 0, 0, 0
		if not self.items:
			frappe.throw("Add some Items before saving")
		for d in self.items:
			cost_price = flt(d.item_quantity) * flt(d.standard_rate)
			self.total_cost_price = self.total_cost_price + cost_price
			self.total_quantity = flt(self.total_quantity) + flt(d.item_quantity)
			self.total_amount = flt(self.total_amount) + flt(d.amount)

	def on_submit(self):
		default_expense_account = frappe.get_value('Company',self.company,'default_expense_account')
		default_inventory_account = frappe.get_value('Company',self.company,'default_inventory_account')
		
		make_gl_entry(self,default_expense_account,self.total_cost_price,flt(0)) #debit account
		make_gl_entry(self,default_inventory_account,flt(0),self.total_cost_price) #credit account

	def on_cancel(self):
		# cancel gl entry
		make_reverse_gl_entry(self,self.doctype,self.name)



@frappe.whitelist()
def get_sales_order_items(name=None):
	parent = frappe.get_doc('Sales Order',name)
	return parent.items