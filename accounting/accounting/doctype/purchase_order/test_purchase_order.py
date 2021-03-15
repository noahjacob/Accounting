# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import nowdate,flt
import unittest

class TestPurchaseOrder(unittest.TestCase):

	def test_new_purchase_order(self):
		p_order = create_purchase_order('Gamestop','Nintendo Switch',1,True,False)
		p_order.append("items",
			{
				"item_name":'Nintendo Switch',
				"item_quantity":1
			})
		p_order.save()
		self.assertTrue(check_created_order(p_order.name),p_order.name)
		total_amount, total_quantity = 0,0
		for d in p_order.items:
			total_quantity+=flt(d.item_quantity)
			total_amount +=flt(d.amount)
		self.assertEqual(p_order.total_amount,total_amount) 
		self.assertEqual(p_order.total_quantity,total_quantity)
		delete_orders(p_order.name)

	def test_validations(self):
		p_order = create_purchase_order('Gamestop','Nintendo Switch',-2,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,p_order.insert)
		delete_orders(p_order.name)
		p_order = create_purchase_order('Gamestop','Nintendo Switch',0,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,p_order.insert)
		delete_orders(p_order.name)
		p_order = create_purchase_order('Gamestop',None,None,False,False)
		self.assertRaises(frappe.exceptions.ValidationError,p_order.insert)
		delete_orders(p_order.name)
		
		


def create_purchase_order(supplier,item_name,qty,save =True,submit = False ):
	p_order = frappe.new_doc('Purchase Order')
	p_order.posting_date = nowdate()
	p_order.supplier = "Gamestop"
	p_order.company = "Test"
	if item_name and qty:
		p_order.set("items",[
			{
				"item_name":item_name,
				"item_quantity":qty
			}
			
		])

	if save or submit:
		p_order.save()
		if submit:
			p_order.submit()
	return p_order



def check_created_order(voucher_no):
	order =  frappe.db.sql("""SELECT
								*
							FROM
								`tabPurchase Order`
							WHERE 
								name = %s""",voucher_no,as_dict = 1)

	return order
def delete_orders(voucher_no):
	frappe.delete_doc("Purchase Order",voucher_no)			

	

