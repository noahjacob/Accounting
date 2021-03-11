# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import flt
import unittest

class TestJournalEntry(unittest.TestCase):
	def test_new_journal_entry(self):
		je = create_journal_entry(100000,100000,True,False)
		self.assertTrue(check_created(je.name))
		self.assertEqual(je.total_credit,100000)
		self.assertEqual(je.total_debit,100000)
		delete(je.name)

	def test_validations(self):
		je = create_journal_entry(None,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,je.insert)
		delete(je.name)
		je = create_journal_entry(10,100,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,je.insert)
		delete(je.name)
		je = create_journal_entry(0,0,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,je.insert)
		delete(je.name)

	
	def test_on_cancel(self):
		je = create_journal_entry(10000,10000,True,True)
		je.cancel()
		gl_entries = get_gl_entries(je.name)
		delete(je.name)
		cancelled_entries = get_cancelled_entries(je.name)
		self.assertTrue(len(cancelled_entries) == 4)
		cancelled_entries = cancelled_entries[:2]
		
		

		expected_reverse_values =[
			{
				'account':'Cash - T',
				'debit_amount':0,
				'credit_amount':10000,
				'is_cancelled':1
			},
			{
				'account':'Owner - T',
				'debit_amount':10000,
				'credit_amount':0,
				'is_cancelled':1
			},
			

		]

		self.assertTrue(cancelled_entries == expected_reverse_values)
		for gle in gl_entries:
			delete_entry(gle.name)

	def test_gl_entry(self):
		je = create_journal_entry(10000,10000,True,True)
		gl_entries = get_gl_entries(je.name)
		self.assertTrue(len(gl_entries) == 2)
		gl_values = gl_entries.copy()
		for d in gl_values:
			del d['name']

		expected_values =[
			{
				'account':'Owner - T',
				'debit_amount':0,
				'credit_amount':10000,
			},
			{
				'account':'Cash - T',
				'debit_amount':10000,
				'credit_amount':0,
			},
			

		]
		self.assertTrue(gl_values == expected_values)

		je.cancel()
		gl_entries = get_gl_entries(je.name)
		delete(je.name)
		
		for gle in gl_entries:
			delete_entry(gle.name)
		
		



def get_gl_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no},fields = ['name','account','debit_amount','credit_amount'])
def get_cancelled_entries(voucher_no):
	return frappe.get_all('GL Entry',filters = {'voucher_no': voucher_no,'is_cancelled':1},fields = ['account','debit_amount','credit_amount','is_cancelled'])
		

def create_journal_entry(credit,debit,save =True,submit = False ):
	je = frappe.new_doc('Journal Entry')
	je.company = "Test"
	if credit and debit:
		je.set("accounts",[
			{
				"account":'Cash - T',
				"debit":debit,
				"credit":0
			},
			{
				"account":'Owner - T',
				"debit":0,
				"credit":credit,
			},	
		])

	if save or submit:
		je.save()
		if submit:
			je.submit()
	return je

def check_created(voucher_no):
	je =  frappe.db.sql("""SELECT
								*
							FROM
								`tabJournal Entry`
							WHERE 
								name = %s""",voucher_no,as_dict = 1)

	return je
def delete(voucher_no):
	frappe.delete_doc("Journal Entry",voucher_no)	

def delete_entry(entry_name):
	frappe.delete_doc("GL Entry",entry_name)