# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import flt,nowdate
import unittest

class TestSalesOrder(unittest.TestCase):
	def test_new_sales_order_totals(self):
		s_order = create_sales_order('Noah','Nintendo Switch',1,30000,True,False)
		s_order.append('items',
		{
				"item_name":'Nintendo Switch',
				"item_quantity":1,
				"delivery_date":nowdate(),
				"item_rate":30000
			},)
		s_order.save()
		self.assertTrue(check_created_order(s_order.name))
		self.assertEqual(s_order.total_cost_price,50000)
		self.assertEqual(s_order.total_amount,60000)
		self.assertEqual(s_order.total_quantity,2)
		delete_orders(s_order.name)



	def test_validations(self):
			s_order = create_sales_order('Noah','Nintendo Switch',-1,30000,False,False)
			self.assertRaises(frappe.exceptions.ValidationError,s_order.insert)
			delete_orders(s_order.name)
			s_order = create_sales_order('Noah','Nintendo Switch',0,30000,False,False)
			self.assertRaises(frappe.exceptions.ValidationError,s_order.insert)
			delete_orders(s_order.name)
			s_order = create_sales_order('Noah',None,None,None,False,False)
			self.assertRaises(frappe.exceptions.ValidationError,s_order.insert)
			delete_orders(s_order.name)


def create_sales_order(customer,item_name,qty,rate,save =True,submit = False ):
	s_order = frappe.new_doc('Sales Order')
	s_order.posting_date = nowdate()
	s_order.customer = customer
	s_order.company = "Test"

	if item_name and qty:
		s_order.set("items",[
			{
				"item_name":item_name,
				"item_quantity":qty,
				"item_rate":rate
			},
			
		])

	if save or submit:
		s_order.save()
		if submit:
			s_order.submit()
	return s_order

def check_created_order(voucher_no):
	order =  frappe.db.sql("""SELECT
								*
							FROM
								`tabSales Order`
							WHERE 
								name = %s""",voucher_no,as_dict = 1)

	return order
def delete_orders(voucher_no):
	frappe.delete_doc("Sales Order",voucher_no)