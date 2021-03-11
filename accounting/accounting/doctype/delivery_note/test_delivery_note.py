# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import flt, nowdate 
import unittest

class TestDeliveryNote(unittest.TestCase):
	def test_new_delivery_note_totals(self):
		dn = create_delivery_note('Noah','Nintendo Switch',1,30000,True,False)
		self.assertTrue(check_created_note(dn.name))
		self.assertEqual(dn.total_cost_price,50000)
		self.assertEqual(dn.total_amount,60000)
		self.assertEqual(dn.total_quantity,2)
		delete_notes(dn.name)
	
	def test_validations(self):
		dn = create_delivery_note('Noah','Nintendo Switch',-1,30000,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,dn.insert)
		delete_notes(dn.name)
		dn = create_delivery_note('Noah','Nintendo Switch',0,30000,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,dn.insert)
		delete_notes(dn.name)
		dn = create_delivery_note('Noah',None,None,None,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,dn.insert)
		delete_notes(dn.name)

	def test_on_cancel(self):

		dn = create_delivery_note('Noah','Nintendo Switch',1,30000,True,True)
		dn.cancel()
		gl_entries = get_gl_entries(dn.name)
		delete_notes(dn.name)
		cancelled_entries = get_cancelled_entries(dn.name)
		self.assertTrue(len(cancelled_entries) == 4)
		cancelled_entries = cancelled_entries[:2]
		
		

		expected_reverse_values =[
			{
				'account':'Cost of Goods Sold - T',
				'debit_amount':0,
				'credit_amount':50000,
				'is_cancelled':1
			},
			{
				'account':'Stock In Hand - T',
				'debit_amount':50000,
				'credit_amount':0,
				'is_cancelled':1
			},

		]

		self.assertTrue(cancelled_entries == expected_reverse_values)
		for gle in gl_entries:
			delete_entry(gle.name)
	
	def test_gl_entry(self):
		dn = create_delivery_note('Noah','Nintendo Switch',1,30000,True,True)
		gl_entries = get_gl_entries(dn.name)
		self.assertTrue(len(gl_entries) == 2)
		gl_values = gl_entries.copy()
		for d in gl_values:
			del d['name']

		expected_values =[
			{
				'account':'Stock In Hand - T',
				'debit_amount':0,
				'credit_amount':50000,
			},
			{
				'account':'Cost of Goods Sold - T',
				'debit_amount':50000,
				'credit_amount':0,
			},
			

		]
		self.assertTrue(gl_values == expected_values)

		dn.cancel()
		gl_entries = get_gl_entries(dn.name)
		delete_notes(dn.name)
		
		for gle in gl_entries:
			delete_entry(gle.name)



def get_gl_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no},fields = ['name','account','debit_amount','credit_amount'])
def get_cancelled_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no,'is_cancelled':1},fields = ['account','debit_amount','credit_amount','is_cancelled'])


def create_delivery_note(customer,item_name,qty,rate,save =True,submit = False ):
	dn = frappe.new_doc('Delivery Note')
	dn.posting_date = nowdate()
	dn.customer = customer
	dn.company = "Test"

	if item_name and qty:
		dn.set("items",[
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
		dn.save()
		if submit:
			dn.submit()
	return dn

def check_created_note(voucher_no):
	note =  frappe.db.sql("""SELECT
								*
							FROM
								`tabDelivery Note`
							WHERE 
								name = %s""",voucher_no,as_dict = 1)

	return note
def delete_notes(voucher_no):
	frappe.delete_doc("Delivery Note",voucher_no)
def delete_entry(entry_name):
	frappe.delete_doc("GL Entry",entry_name)
