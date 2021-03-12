# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt

class PaymentEntry(Document):
	def validate(self):
		self.amount_paid = 0
		for d in self.payment_references:
			self.amount_paid = self.amount_paid + flt(d.amount)
		if self.payment_type == "Pay":
			account_paid_to = frappe.get_value('Company',self.company,'default_payable_account')
			account_paid_from = frappe.get_value('Company',self.company,'default_cash_account')
			self.account_paid_to = account_paid_to
			self.account_paid_from  = account_paid_from
		elif self.payment_type == "Receive":
			account_paid_to = frappe.get_value('Company',self.company,'default_cash_account')
			account_paid_from = frappe.get_value('Company',self.company,'default_receivable_account')
			self.account_paid_to = account_paid_to
			self.account_paid_from  = account_paid_from
	
		
		
	
	def on_submit(self):
		if self.payment_type == "Pay":
			account_paid_to = frappe.get_value('Company',self.company,'default_payable_account')
			account_paid_from = frappe.get_value('Company',self.company,'default_cash_account')
			self.account_paid_to = account_paid_to
			self.account_paid_from  = account_paid_from
			make_gl_entry(self,self.account_paid_to,self.amount_paid,flt(0)) #debit account
			make_gl_entry(self,self.account_paid_from,flt(0),self.amount_paid) #credit account
		else:
			account_paid_to = frappe.get_value('Company',self.company,'default_cash_account')
			account_paid_from = frappe.get_value('Company',self.company,'default_receivable_account')
			self.account_paid_to = account_paid_to
			self.account_paid_from  = account_paid_from
			make_gl_entry(self,self.account_paid_to,self.amount_paid,flt(0)) #debit account
			make_gl_entry(self,self.account_paid_from,flt(0),self.amount_paid) #credit account

	def on_cancel(self):
		# cancel gl entry
		make_reverse_gl_entry(self,self.doctype,self.name)

