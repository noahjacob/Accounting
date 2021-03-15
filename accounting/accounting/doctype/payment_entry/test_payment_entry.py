# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import flt
import unittest
from accounting.accounting.doctype.purchase_invoice.test_purchase_invoice import create_purchase_invoice ,delete,delete_entry,get_gl_entries,get_cancelled_entries
from accounting.accounting.doctype.sales_invoice.test_sales_invoice import create_sales_invoice ,delete_si

class TestPaymentEntry(unittest.TestCase):
	def test_new_payment_pay(self):
		pi = create_purchase_invoice("Gamestop","Nintendo Switch",1,True,True)
		pe = create_payment_entry("Pay","Purchase Invoice",pi.name,True,False)
		self.assertTrue(check_created(pe.name))
		self.assertEqual(pe.amount_paid,25000)
		self.assertEqual(pe.account_paid_from,"Cash - T")
		self.assertEqual(pe.account_paid_to,"Creditors - T")

		delete_pe(pe.name)
		pi.cancel()
		entries = get_gl_entries(pi.name)
		for e in entries:
			delete_entry(e.name)
		delete(pi.name)


	def test_payment_pay_posting_entry(self):
		pi = create_purchase_invoice("Gamestop","Nintendo Switch",1,True,True)
		pe = create_payment_entry("Pay","Purchase Invoice",pi.name,True,True)
		gl_entries = get_gl_entries(pe.name)
		self.assertTrue(len(gl_entries) == 2)
		gl_values = gl_entries.copy()
		for d in gl_values:
			del d['name']

		expected_values =[
			{
				'account':'Cash - T',
				'debit_amount':0,
				'credit_amount':25000,
			},
			{
				'account':'Creditors - T',
				'debit_amount':25000,
				'credit_amount':0,
			},
			

		]
		self.assertEqual(expected_values,gl_values)
		
		pe.cancel()
		pe_entries = get_gl_entries(pe.name)
		delete_pe(pe.name)

		for pe in pe_entries:
			delete_entry(pe.name)

		pi.cancel()
		gl_entries = get_gl_entries(pi.name)
		delete(pi.name)
		
		for gle in gl_entries:
			delete_entry(gle.name)


	def test_payment_pay_posting_cancel(self):
		pi = create_purchase_invoice("Gamestop","Nintendo Switch",1,True,True)
		pe = create_payment_entry("Pay","Purchase Invoice",pi.name,True,True)
		
		pe.cancel()
		gl_entries = get_gl_entries(pe.name)
		delete_pe(pe.name)
		cancelled_entries = get_cancelled_entries(pe.name)
		self.assertTrue(len(cancelled_entries) == 4)
		cancelled_entries = cancelled_entries[:2]
		
		

		expected_reverse_values =[
			{
				'account':'Creditors - T',
				'debit_amount':0,
				'credit_amount':25000,
				'is_cancelled':1
			},
			{
				'account':'Cash - T',
				'debit_amount':25000,
				'credit_amount':0,
				'is_cancelled':1
			},
			

		]

		self.assertTrue(cancelled_entries == expected_reverse_values)
		for gle in gl_entries:
			delete_entry(gle.name)
		
		pi.cancel()
		gl_entries = get_gl_entries(pi.name)
		delete_si(pi.name)

		for gle in gl_entries:
			delete_entry(gle.name)
	


	def test_new_payment_receive(self):
		si = create_sales_invoice("Noah","Nintendo Switch",1,30000,True,True)
		pe = create_payment_entry("Receive","Sales Invoice",si.name,True,False)
		self.assertTrue(check_created(pe.name))
		self.assertEqual(pe.amount_paid,30000)
		self.assertEqual(pe.account_paid_from,"Debtors - T")
		self.assertEqual(pe.account_paid_to,"Cash - T")
		delete_pe(pe.name)
		si.cancel()
		entries = get_gl_entries(si.name)
		for e in entries:
			delete_entry(e.name)
		delete_si(si.name)

	def test_payment_receive_posting_cancel(self):
		si = create_sales_invoice('Noah','Nintendo Switch',1,30000,True,True)
		pe = create_payment_entry("Receive","Sales Invoice",si.name,True,True)
		
		pe.cancel()
		gl_entries = get_gl_entries(pe.name)
		delete_pe(pe.name)
		cancelled_entries = get_cancelled_entries(pe.name)
		self.assertTrue(len(cancelled_entries) == 4)
		cancelled_entries = cancelled_entries[:2]
		
		

		expected_reverse_values =[
			{
				'account':'Cash - T',
				'debit_amount':0,
				'credit_amount':30000,
				'is_cancelled':1
			},
			{
				'account':'Debtors - T',
				'debit_amount':30000,
				'credit_amount':0,
				'is_cancelled':1
			},
			

		]

		self.assertTrue(cancelled_entries == expected_reverse_values)
		for gle in gl_entries:
			delete_entry(gle.name)
		
		si.cancel()
		gl_entries = get_gl_entries(si.name)
		delete_si(si.name)

		for gle in gl_entries:
			delete_entry(gle.name)

	def test_payment_receive_posting_entry(self):
		si = create_sales_invoice('Noah','Nintendo Switch',1,30000,True,True)
		pe = create_payment_entry("Receive","Sales Invoice",si.name,True,True)
		gl_entries = get_gl_entries(pe.name)
		self.assertTrue(len(gl_entries) == 2)
		gl_values = gl_entries.copy()
		for d in gl_values:
			del d['name']

		expected_values =[
			{
				'account':'Debtors - T',
				'debit_amount':0,
				'credit_amount':30000,
			},
			{
				'account':'Cash - T',
				'debit_amount':30000,
				'credit_amount':0,
			},
			

		]
		self.assertEqual(expected_values,gl_values)
		
		pe.cancel()
		pe_entries = get_gl_entries(pe.name)
		delete_pe(pe.name)

		for pe in pe_entries:
			delete_entry(pe.name)

		si.cancel()
		gl_entries = get_gl_entries(si.name)
		delete_si(si.name)
		
		for gle in gl_entries:
			delete_entry(gle.name)


def create_payment_entry(pay_type,invoice_type,name,save =True,submit = False ):
	pe = frappe.new_doc('Payment Entry')
	pe.company = "Test"
	if pay_type == "Pay":
		pe.payment_type = "Pay"
		pe.set('payment_references',[
			{
			"reference_type":invoice_type,
			"reference_name":name,
			
		}
		])
	else:
		pe.payment_type = "Receive"
		
		pe.set('payment_references',[
			{
			"reference_type":invoice_type,
			"reference_name":name,
			
		}
		])
		

	

	if save or submit:
		pe.save()
		if submit:
			pe.submit()
	return pe

def delete_pe(voucher_no):
	frappe.delete_doc("Payment Entry",voucher_no)	

def check_created(voucher_no):
	pe =  frappe.db.sql("""SELECT
								*
							FROM
								`tabPayment Entry`
							WHERE 
								name = %s""",voucher_no,as_dict = 1)

	return pe

