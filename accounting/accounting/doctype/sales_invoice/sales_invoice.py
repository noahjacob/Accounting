# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt



class SalesInvoice(Document):
	def validate(self):
		calculate_totals(self)
		validate_quantity(self)
		


	def on_submit(self):
		default_receivable_account = frappe.get_value('Company',self.company,'default_receivable_account')
		default_income_account = frappe.get_value('Company',self.company,'default_income_account')
		
		make_gl_entry(self,default_receivable_account,self.total_amount,flt(0)) #debit account
		make_gl_entry(self,default_income_account,flt(0),self.total_amount) #credit account

	def on_cancel(self):
		# cancel gl entry
		make_reverse_gl_entry(self,self.doctype,self.name)

def calculate_totals(self):
	self.total_amount, self.total_quantity = 0, 0
	if not self.items:
		frappe.throw("Add some Items before saving")
	for d in self.items:
		d.amount = d.item_quantity * d.item_rate
		self.total_quantity = flt(self.total_quantity) + flt(d.item_quantity)
		self.total_amount = flt(self.total_amount) + flt(d.amount)

def validate_quantity(self):
	for d in self.items:
		if d.item_quantity < 0 or d.item_quantity == 0:
			frappe.throw("Item quantity is invalid")

@frappe.whitelist()
def add_to_cart(user,item_name,qty):
	check = check_cart(user)
	print(check)
	if not check:
		create_sales_invoice(user,item_name,qty)
	else:
		print(check[0]['name'])
		si = frappe.get_doc('Sales Invoice',check[0]['name'])
		print("ajksbdas",item_name)
		si.append("items",{
			'item_name':item_name,
			'item_quantity':flt(qty)
		})
		si.save()
@frappe.whitelist()
def update_cart(user,index,buy = False, submit = False):
	check = check_cart(user)
	index = int(index)
	cart = frappe.get_doc('Sales Invoice',check[0]['name'])
	for idx,item in enumerate(cart.items):
		
		if idx == index:
			if buy:
				create_sales_invoice(user,item.item_name,item.item_quantity,submit = True)
			
			cart.remove(item)
			break
	if not len(cart.items):
		frappe.delete_doc('Sales Invoice',check[0]['name'])
	else:
		cart.save()
@frappe.whitelist()
def create_sales_invoice(user,item_name,qty,save = True,submit = False):
	si = frappe.new_doc('Sales Invoice')
	si.customer = user
	si.company = "Test"
	si.set("items",[{
		'item_name':item_name,
		'item_quantity':flt(qty)
	}])
	if save or submit:
		si.save()
		if submit:
			si.submit()

@frappe.whitelist()		
def check_cart(user):
	
	check = frappe.db.get_list('Sales Invoice',filters = {'docstatus':0,'customer':user})
	return check

	