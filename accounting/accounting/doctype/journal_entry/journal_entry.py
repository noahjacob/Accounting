# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry

class JournalEntry(Document):

	def validate(self):
		calc_total_debit_credit(self)
		if self.difference:
			frappe.throw("The total debit and credit must be equal. The current difference is {}".format(self.difference))
		if self.total_credit == 0 or self.total_debit == 0 :
			frappe.throw('Total Cannot be Zero')
		if not self.accounts:
			frappe.throw('Account Entries are required')
		else:
			self.title = self.accounts[0].account





	def on_submit(self):
		for entry in self.accounts:
			make_gl_entry(self,entry.account,entry.debit,entry.credit)
			

	def on_cancel(self):
		# cancel gl entry
		make_reverse_gl_entry(self,self.doctype,self.name)
		
	
def calc_total_debit_credit(self):
	self.total_debit, self.total_credit,self.difference = 0,0,0
	for entry in self.accounts:
		self.total_debit = flt(self.total_debit) +flt(entry.debit) 
		self.total_credit = flt(self.total_credit) + flt(entry.credit)

	self.difference = flt(self.total_debit) - (self.total_credit)