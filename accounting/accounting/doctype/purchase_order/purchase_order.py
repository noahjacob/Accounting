# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt
class PurchaseOrder(Document):
	def validate(self):
		self.total_amount,self.total_quantity = 0,0
		if not self.items:
			frappe.throw("Add some Items before saving")
		for d in self.items:
			self.total_quantity = flt(self.total_quantity) + flt(d.item_quantity)
			self.total_amount = flt(self.total_amount) + flt(d.amount)

	
		
			
