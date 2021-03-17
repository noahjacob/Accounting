# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

class TestCompany(unittest.TestCase):
	def test_create_company(self):
		c = create_company('Test Company')
		
		self.assertEqual(c.company_name,'Test Company')
		self.assertEqual(c.abbr,'TC')
		validate_default_accounts(self,c)
		c = create_company('Test Company',save=False)
		self.assertRaises(frappe.exceptions.ValidationError,c.insert)

	
	
	def tearDown(self):
		c = frappe.get_doc('Company','Test Company')
		c = clear_accounts(c)
		delete_accounts('Test Company')
		frappe.delete_doc('Company','Test Company')
		
		

def create_company(name,save = True):
	c = frappe.new_doc('Company')
	c.company_name = name
	if save:
		c.save()
	return c
def clear_accounts(c):
	c.default_inventory_account = ""
	c.default_cash_account = ""
	c.default_payable_account = "" 
	c.default_receivable_account = "" 
	c.default_expense_account = "" 
	c.default_income_account = "" 
	c.default_inventory_account = "" 
	c.stock_received_but_not_billed = ""
	c.save()
	return c 
def validate_default_accounts(self,c):
	self.assertEqual(c.default_inventory_account,"Stock In Hand - TC"),
	self.assertEqual(c.default_cash_account, 'Cash - TC')
	self.assertEqual(c.default_payable_account, 'Creditors - TC')
	self.assertEqual(c.default_receivable_account, 'Debtors - TC')
	self.assertEqual(c.default_expense_account, 'Cost of Goods Sold - TC')
	self.assertEqual(c.default_income_account, 'Sales - TC')
	self.assertEqual(c.default_inventory_account, 'Stock In Hand - TC')
	self.assertEqual(c.stock_received_but_not_billed, 'Stock Received But Not Billed - TC')

def delete_accounts(company):
	
	accounts = frappe.get_all('Account',filters = {'company': company},fields = ['name'])
	
	for d in accounts:

		frappe.db.sql("""DELETE
					FROM
						tabAccount
					WHERE
						name = %s
					""",d.name)
