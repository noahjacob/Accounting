# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt

class PaymentEntry(Document):
	def before_save(self):
		self.amount_paid = 0
		for d in self.payment_references:
			self.amount_paid = self.amount_paid + flt(d.amount)
		
		
	
	def on_submit(self):
		if self.payment_type == "Pay":
			make_gl_entry(self,self.account_paid_to,self.amount_paid,flt(0)) #debit account
			make_gl_entry(self,self.account_paid_from,flt(0),self.amount_paid) #credit account
		else:
			make_gl_entry(self,self.account_paid_to,self.amount_paid,flt(0)) #debit account
			make_gl_entry(self,self.account_paid_from,flt(0),self.amount_paid) #credit account

	def on_cancel(self):
		# cancel gl entry
		make_reverse_gl_entry(self,self.doctype,self.name)

