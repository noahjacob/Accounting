# Copyright (c) 2013, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	asset = get_data(filters.company,'Asset')
	liability = get_data(filters.company,'Liability')
	data.extend(asset)
	data.extend(liability)

	return columns, data

def get_data(company,account_type):
	accounts = get_accounts(company,account_type)
	data = []
	
	indent = 0
	for d in accounts:
		if d.parent_account == None or d.parent_account == data[-1]['account']:
			data_add(data,d,indent)
			indent = indent +1
		else:
			for n in data:
				if n['account'] == d.parent_account:
					indent = n['indent'] + 1
					data_add(data,d,indent)
					break
			indent = indent + 1
			
	return data
		



def data_add(data,account,indent):
	data.append({
		"account":account.name,
		"parent_account":account.parent_account,
		"account_type":account.account_type,
		"has_value":account.is_group,
		"indent":indent,
		"amount":0
	})

def get_accounts(company,account_type):
	return frappe.db.sql("""SELECT
								name,parent_account,lft,is_group,account_type
							FROM
								tabAccount
							WHERE
								company = %s and account_type = %s
							ORDER BY
								lft""",(company,account_type),as_dict = 1)
def get_columns():
	columns = [
		{
			"fieldname": "account",
			"label": "Account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 300
		},
		{
			"fieldname": 'amount',
			"label": 'Amount',
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100
		}
	]
	return columns