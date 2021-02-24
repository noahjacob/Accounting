# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt



class SalesInvoice(Document):
	def on_submit(self):
		default_receivable_account = frappe.get_value('Company',self.company,'default_receivable_account')
		default_income_account = frappe.get_value('Company',self.company,'default_income_account')
		
		make_gl_entry(self,default_receivable_account,self.total_amount,flt(0)) #debit account
		make_gl_entry(self,default_income_account,flt(0),self.total_amount) #credit account
