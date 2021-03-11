# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import flt,nowdate
import unittest

class TestPurchaseInvoice(unittest.TestCase):
	def test_new_purchase_invoice(self):
		pi = create_purchase_invoice('Gamestop','Nintendo Switch',2,True,False)
		self.assertTrue(check_created(pi.name),pi.name)
		self.assertEqual(pi.total_amount,100000)
		self.assertEqual(pi.total_quantity,4)
		delete(pi.name)


	def test_validations(self):
		pi = create_purchase_invoice('Gamestop','Nintendo Switch',-2,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,pi.insert)
		delete(pi.name)
		pi = create_purchase_invoice('Gamestop','Nintendo Switch',0,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,pi.insert)
		delete(pi.name)
		pi = create_purchase_invoice('Gamestop',None,None,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,pi.insert)
		delete(pi.name)
	
	def test_on_cancel(self):
		pi = create_purchase_invoice('Gamestop','Nintendo Switch',1,True,True)
		pi.cancel()
		gl_entries = get_gl_entries(pi.name)
		delete(pi.name)
		cancelled_entries = get_cancelled_entries(pi.name)
		self.assertTrue(len(cancelled_entries) == 4)
		cancelled_entries = cancelled_entries[:2]
		
		

		expected_reverse_values =[
			{
				'account':'Stock Received But Not Billed - T',
				'debit_amount':0,
				'credit_amount':50000,
				'is_cancelled':1
			},
			{
				'account':'Creditors - T',
				'debit_amount':50000,
				'credit_amount':0,
				'is_cancelled':1
			},

		]

		self.assertTrue(cancelled_entries == expected_reverse_values)
		for gle in gl_entries:
			delete_entry(gle.name)


	def test_gl_entry(self):
		pi = create_purchase_invoice('Gamestop','Nintendo Switch',1,True,True)
		gl_entries = get_gl_entries(pi.name)
		self.assertTrue(len(gl_entries) == 2)
		gl_values = gl_entries.copy()
		for d in gl_values:
			del d['name']

		expected_values =[
			{
				'account':'Creditors - T',
				'debit_amount':0,
				'credit_amount':50000,
			},
			{
				'account':'Stock Received But Not Billed - T',
				'debit_amount':50000,
				'credit_amount':0,
			},
			

		]
		self.assertTrue(gl_values == expected_values)

		pi.cancel()
		gl_entries = get_gl_entries(pi.name)
		delete(pi.name)
		
		for gle in gl_entries:
			delete_entry(gle.name)
		
		



def get_gl_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no},fields = ['name','account','debit_amount','credit_amount'])
def get_cancelled_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no,'is_cancelled':1},fields = ['account','debit_amount','credit_amount','is_cancelled'])


def create_purchase_invoice(supplier,item_name,qty,save =True,submit = False ):
	pi = frappe.new_doc('Purchase Invoice')
	pi.posting_date = nowdate()
	pi.supplier = "Gamestop"
	pi.company = "Test"
	if item_name and qty:
		pi.set("items",[
			{
				"item_name":item_name,
				"item_quantity":qty
			},
			{
				"item_name":item_name,
				"item_quantity":qty
			},
		])

	if save or submit:
		pi.save()
		if submit:
			pi.submit()
	return pi



def check_created(voucher_no):
	order =  frappe.db.sql("""SELECT
								*
							FROM
								`tabPurchase Invoice`
							WHERE 
								name = %s""",voucher_no,as_dict = 1)

	return order
def delete(voucher_no):
	frappe.delete_doc("Purchase Invoice",voucher_no)		

def delete_entry(entry_name):
	frappe.delete_doc("GL Entry",entry_name)
