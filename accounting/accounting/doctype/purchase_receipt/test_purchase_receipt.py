# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import flt, nowdate
import unittest

class TestPurchaseReceipt(unittest.TestCase):
	def test_new_purchase_receipt(self):
		pr = create_purchase_receipt('Gamestop','Nintendo Switch',2,True,False)
		pr.append('items',
		{
				"item_name":'Nintendo Switch',
				"item_quantity":2
			})
		pr.save()
		self.assertTrue(check_created(pr.name),pr.name)
		self.assertEqual(pr.total_amount,100000)
		self.assertEqual(pr.total_quantity,4)
		delete(pr.name)


	def test_validations(self):
		pr = create_purchase_receipt('Gamestop','Nintendo Switch',-2,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,pr.insert)
		delete(pr.name)
		pr = create_purchase_receipt('Gamestop','Nintendo Switch',0,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,pr.insert)
		delete(pr.name)
		pr = create_purchase_receipt('Gamestop',None,None,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,pr.insert)
		delete(pr.name)
	
	def test_on_cancel(self):
		pr = create_purchase_receipt('Gamestop','Nintendo Switch',2,True,True)
		pr.cancel()
		gl_entries = get_gl_entries(pr.name)
		delete(pr.name)
		cancelled_entries = get_cancelled_entries(pr.name)
		self.assertTrue(len(cancelled_entries) == 4)
		cancelled_entries = cancelled_entries[:2]
		
		

		expected_reverse_values =[
			{
				'account':'Stock In Hand - T',
				'debit_amount':0,
				'credit_amount':50000,
				'is_cancelled':1
			},
			{
				'account':'Stock Received But Not Billed - T',
				'debit_amount':50000,
				'credit_amount':0,
				'is_cancelled':1
			},

		]

		self.assertTrue(cancelled_entries == expected_reverse_values)
		for gle in gl_entries:
			delete_entry(gle.name)


	def test_gl_entry(self):
		pr = create_purchase_receipt('Gamestop','Nintendo Switch',2,True,True)
		gl_entries = get_gl_entries(pr.name)
		self.assertTrue(len(gl_entries) == 2)
		gl_values = gl_entries.copy()
		for d in gl_values:
			del d['name']

		expected_values =[
			{
				'account':'Stock Received But Not Billed - T',
				'debit_amount':0,
				'credit_amount':50000,
			},
			{
				'account':'Stock In Hand - T',
				'debit_amount':50000,
				'credit_amount':0,
			},
			

		]
		self.assertTrue(gl_values == expected_values)

		pr.cancel()
		gl_entries = get_gl_entries(pr.name)
		delete(pr.name)
		
		for gle in gl_entries:
			delete_entry(gle.name)
		
		



def get_gl_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no},fields = ['name','account','debit_amount','credit_amount'])
def get_cancelled_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no,'is_cancelled':1},fields = ['account','debit_amount','credit_amount','is_cancelled'])


def create_purchase_receipt(supplier,item_name,qty,save =True,submit = False ):
	pr = frappe.new_doc('Purchase Receipt')
	pr.posting_date = nowdate()
	pr.supplier = "Gamestop"
	pr.company = "Test"
	if item_name and qty:
		pr.set("items",[
			{
				"item_name":item_name,
				"item_quantity":qty
			},
			
		])

	if save or submit:
		pr.save()
		if submit:
			pr.submit()
	return pr



def check_created(voucher_no):
	order =  frappe.db.sql("""SELECT
								*
							FROM
								`tabPurchase Receipt`
							WHERE 
								name = %s""",voucher_no,as_dict = 1)

	return order
def delete(voucher_no):
	frappe.delete_doc("Purchase Receipt",voucher_no)		

def delete_entry(entry_name):
	frappe.delete_doc("GL Entry",entry_name)