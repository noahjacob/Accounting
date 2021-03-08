# Copyright (c) 2013, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	columns, data = [], []
	
	date=[]
	if filters.get('filter_based_on') =='Date Range':
		date.append(filters.get('from_date'))
		date.append(filters.get('to_date'))
		from_year = (date[0].split("-"))[0]
		to_year = (date[1].split("-"))[0]
		labels = from_year if from_year == to_year else from_year + "-" + to_year 
	else:
		get_fiscal_year(date,filters)
		labels = filters.get("fiscal_year")

	columns = get_columns(labels)
	
	validate_dates(date)
	income = get_data(filters.company,'Income',date)
	expense = get_data(filters.company,'Expense',date)
	
	data.extend(income)
	data.extend(expense)
	
	get_total_profit_loss(data)
	chart = get_chart_data(filters,columns,income,expense,data[-1])
	report_summary = get_report_summary(income[-2],expense[-2],data[-1])
	return columns, data, None, chart, report_summary 

def get_chart_data(filters,columns,income,expense,profit_loss):
	labels = [d.get("label") for d in columns[1:]]

	income_data, expense_data,profit_loss_data = [], [], []

	
	if income:
		income_data.append(income[-2].get("amount"))
	if expense:
		expense_data.append(expense[-2].get("amount"))
	if profit_loss:
		profit_loss_data.append(profit_loss.get("amount"))	
		

	datasets = []
	if income_data:
		datasets.append({'name': ('Income'), 'values': income_data})
	if expense_data:
		datasets.append({'name': ('Expense'), 'values': expense_data})
	if profit_loss_data:
		datasets.append({'name': ('Net Profit/Loss'), 'values': profit_loss_data})
	

	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}

	if filters.chart_type == "Bar":
		chart["type"] = "bar"
	else:
		chart["type"] = "line"

	return chart

def get_report_summary(income,expense,profit_loss):
	return [
		{
			"value": income['amount'],
			"label": "Total Income This Year",
			"datatype": "Currency",
			"currency": "₹"
		},
		{
			"value": expense['amount'],
			"label": "Total Expense This Year",
			"datatype": "Currency",
			"currency": "₹"
		},
		
		{
			"value":profit_loss['amount'],
			"label": "Profit/Loss This Year",
			"indicator": "Green" if profit_loss['amount'] > 0 else "Red" ,
			"datatype": "Currency",
			"currency": "₹"
		}
	]

def validate_dates(date):
	if date[0] > date[1]:
		frappe.throw("Starting Date cannot be greater than ending date")

def get_fiscal_year(date,filters):
	dates = frappe.db.sql("""SELECT
								from_date,to_date
							FROM
								`tabFiscal Year`
							WHERE
								period = %(fiscal_year)s		
								""",filters,as_dict = 1)[0]
	date.append(dates.get('from_date'))
	date.append(dates.get('to_date'))

def get_data(company,account_type,date):
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
	root_type = "Income" if account_type == "Income" else "Expenses"
	
	get_account_balances(company,data,root_type,date)
		
	return data
		

def get_account_balances(company,accounts,root_type,date):
	data = []
	
	for a in accounts:
		if not a['has_value']:
			amount  = get_balance(company,a['account'],date)
			amount = amount if amount  else 0.0
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
		'account':'Total ' + accounts[0]['account_type'] + (' (' + "Debit" + ')' if accounts[0]['account_type'] == 'Expense' else ' ('+'Credit' +')'),
		'amount':accounts[0]['amount']
		}
	accounts.append(total_credit_debit)
	accounts.append({})

def get_total_profit_loss(data):
	total_debit = data[0]['amount']
	total_credit = data[-2]['amount']
	total_profit_loss = total_debit - abs(total_credit)
	total_credit += total_profit_loss
	data.append({'account':'Profit/Loss for the year','amount':total_profit_loss})
	

	
def get_balance(company,name,date):
	return frappe.db.sql("""SELECT
								sum(credit_amount) - sum(debit_amount) as total
							FROM
								`tabGL Entry`
							WHERE
								company = %s and account = %s and posting_date >= %s and posting_date <= %s
						""",(company,name,date[0],date[1]),as_dict = 1)[0]['total']
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
def get_columns(labels):
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
			"label": labels,
			"fieldtype": "Currency",
			"options": "currency",
			"width": 500
		}
	]
	return columns
