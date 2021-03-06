# -*- coding: utf-8 -*-
# Copyright (c) 2021, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils.nestedset import NestedSet


class Account(NestedSet):
	nsm_parent_field = "parent_account"
	def validate(self):
		self.account_name = self.account_name +' - '+ self.company[0]
		

		
	
	
@frappe.whitelist()	
def get_children(doctype, parent=None, company=None, is_root=False):
	if is_root:
		parent = ""

	fields = ['name as value', 'is_group as expandable']
	filters = [
		['docstatus','<','2'],
		['ifnull(`parent_account`, "")', '=', parent],
		['company', '=', company]
	]
	
	accounts = frappe.get_list(doctype, fields=fields, filters=filters, order_by='name')
	return accounts
