# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt
class PurchaseOrder(Document):
	def validate(self):
		calc_totals(self)
		validate_quantity(self)


		
	
def calc_totals(self):
	self.total_amount,self.total_quantity = 0,0
	if not self.items:
		frappe.throw("Add some Items before saving")
	for d in self.items:
		d.amount = d.item_quantity * d.item_rate
	for d in self.items:
		self.total_quantity = flt(self.total_quantity) + flt(d.item_quantity)
		self.total_amount = flt(self.total_amount) + flt(d.amount)

def validate_quantity(self):
	for d in self.items:
		if d.item_quantity < 0 or d.item_quantity == 0:
			frappe.throw("Item quantity is invalid")

		
			
