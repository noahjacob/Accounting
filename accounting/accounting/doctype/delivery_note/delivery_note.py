# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt


class DeliveryNote(Document):
	def on_submit(self):
		default_expense_account = frappe.get_value('Company',self.company,'default_expense_account')
		default_inventory_account = frappe.get_value('Company',self.company,'default_inventory_account')
		
		make_gl_entry(self,default_expense_account,self.total_cost_price,flt(0)) #debit account
		make_gl_entry(self,default_inventory_account,flt(0),self.total_cost_price) #credit account




@frappe.whitelist()
def get_sales_order_items(name=None):
	parent = frappe.get_doc('Sales Order',name)
	return parent.items