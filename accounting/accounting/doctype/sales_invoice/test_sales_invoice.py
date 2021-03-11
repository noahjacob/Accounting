# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import flt, nowdate
import unittest

class TestSalesInvoice(unittest.TestCase):
	def test_new_sales_invoice_totals(self):
		si = create_sales_invoice('Noah','Nintendo Switch',1,30000,True,False)
		self.assertTrue(check_created(si.name))
		self.assertEqual(si.total_amount,60000)
		self.assertEqual(si.total_quantity,2)
		delete(si.name)
	
	def test_validations(self):
		si = create_sales_invoice('Noah','Nintendo Switch',-1,30000,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,si.insert)
		delete(si.name)
		si = create_sales_invoice('Noah','Nintendo Switch',0,30000,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,si.insert)
		delete(si.name)
		si = create_sales_invoice('Noah',None,None,None,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,si.insert)
		delete(si.name)

	def test_on_cancel(self):

		si = create_sales_invoice('Noah','Nintendo Switch',1,30000,True,True)
		si.cancel()
		gl_entries = get_gl_entries(si.name)
		delete(si.name)
		cancelled_entries = get_cancelled_entries(si.name)
		self.assertTrue(len(cancelled_entries) == 4)
		cancelled_entries = cancelled_entries[:2]
		
		

		expected_reverse_values =[
			{
				'account':'Debtors - T',
				'debit_amount':0,
				'credit_amount':60000,
				'is_cancelled':1
			},
			{
				'account':'Sales - T',
				'debit_amount':60000,
				'credit_amount':0,
				'is_cancelled':1
			},

		]

		self.assertTrue(cancelled_entries == expected_reverse_values)
		for gle in gl_entries:
			delete_entry(gle.name)
	
	def test_gl_entry(self):
		si = create_sales_invoice('Noah','Nintendo Switch',1,30000,True,True)
		gl_entries = get_gl_entries(si.name)
		self.assertTrue(len(gl_entries) == 2)
		gl_values = gl_entries.copy()
		for d in gl_values:
			del d['name']

		expected_values =[
			{
				'account':'Sales - T',
				'debit_amount':0,
				'credit_amount':60000,
			},
			{
				'account':'Debtors - T',
				'debit_amount':60000,
				'credit_amount':0,
			},
			

		]
		self.assertTrue(gl_values == expected_values)

		si.cancel()
		gl_entries = get_gl_entries(si.name)
		delete(si.name)
		
		for gle in gl_entries:
			delete_entry(gle.name)



def get_gl_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no},fields = ['name','account','debit_amount','credit_amount'])
def get_cancelled_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no,'is_cancelled':1},fields = ['account','debit_amount','credit_amount','is_cancelled'])

def create_sales_invoice(customer,item_name,qty,rate,save =True,submit = False ):
	si = frappe.new_doc('Sales Invoice')
	si.posting_date = nowdate()
	si.customer = customer
	si.company = "Test"

	if item_name and qty:
		si.set("items",[
			{
				"item_name":item_name,
				"item_quantity":qty,
				"item_rate":rate
			},
			{
				"item_name":item_name,
				"item_quantity":qty,
				"item_rate":rate
			},
		])

	if save or submit:
		si.save()
		if submit:
			si.submit()
	return si

def check_created(voucher_no):
	note =  frappe.db.sql("""SELECT
								*
							FROM
								`tabSales Invoice`
							WHERE 
								name = %s""",voucher_no,as_dict = 1)

	return note
def delete(voucher_no):
	frappe.delete_doc("Sales Invoice",voucher_no)
def delete_entry(entry_name):
	frappe.delete_doc("GL Entry",entry_name)