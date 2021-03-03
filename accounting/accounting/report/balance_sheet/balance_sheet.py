# Copyright (c) 2013, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	asset = get_data(filters.company,'Asset')
	liability = get_data(filters.company,'Liability')
	data.extend(asset)
	data.extend(liability)
	get_total_profit_loss(data)

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
	root_type = "Assets" if account_type == "Asset" else "Liabilities"
	
	get_account_balances(company,data,root_type)
		
	return data
		

def get_account_balances(company,accounts,root_type):
	data = []
	
	for a in accounts:
		if not a['has_value']:
			amount  = get_balance(company,a['account'])
			amount  = abs(amount)
			a['amount'] = amount
			
			for d in reversed(data):
				if d['parent_account'] == root_type:
					d['amount'] +=flt(amount)
					data[0]['amount']+=flt(amount) 
					break
				else:
					d['amount'] +=flt(amount)

			
			data.append(a)
			
		else:
			data.append(a)
	
	total_credit_debit = {
		'account':'Total ' + accounts[0]['account_type'] + (' (' + "Debit" + ')' if accounts[0]['account_type'] == 'Asset' else ' ('+'Credit' +')'),
		'amount':accounts[0]['amount']
		}
	accounts.append(total_credit_debit)
	accounts.append({})

def get_total_profit_loss(data):
	total_debit = data[0]['amount']
	total_credit = data[-2]['amount']
	total_profit_loss = total_debit - total_credit
	total_credit += total_profit_loss
	data.append({'account':'Provisonal Profit/Loss(Credit)','amount':total_profit_loss})
	data.append({'account':'Total(Credit)','amount':total_credit}) 

	
def get_balance(company,name):
	return frappe.db.sql("""SELECT
								sum(debit_amount) - sum(credit_amount) as total
							FROM
								`tabGL Entry`
							WHERE
								company = %s and account = %s
						""",(company,name),as_dict = 1)[0]['total']
def data_add(data,account,indent):
	data.append({
		"account":account.name,
		"parent_account":account.parent_account,
		"account_type":account.account_type,
		"has_value":account.is_group,
		"indent":indent,
		"amount":0.0
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
			"width": 400
		},
		{
			"fieldname": 'amount',
			"label": 'Amount',
			"fieldtype": "Currency",
			"options": "currency",
			"width": 500
		}
	]
	return columns