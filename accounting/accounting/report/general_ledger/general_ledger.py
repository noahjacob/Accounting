# Copyright (c) 2013, Noah Jacob and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, _dict
from frappe.utils import flt

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	gl_entries = get_gl_entries(filters)
	all_entries = get_totaled_entries(filters,gl_entries)
	data = set_balance_in_entries(all_entries)
	return columns, data

def get_gl_entries(filters):
	gl_entries = frappe.db.sql("""SELECT 
									name as gl_entry, posting_date,account,voucher_type,voucher_no,debit_amount,credit_amount

								FROM
									`tabGL Entry`
								WHERE
									{conditions}
								ORDER BY
									posting_date
								""".format(conditions = get_conditions(filters)),filters,as_dict = 1)
	return gl_entries

def get_totals(filters,gl_entries):
	opening = get_opening_closing_total_values('Opening')
	closing = get_opening_closing_total_values('Closing (Opening + Total)')
	total = get_opening_closing_total_values('Total')

	for entry in gl_entries:
		total.debit_amount += flt(entry.debit_amount)
		total.credit_amount += flt(entry.credit_amount)
		closing.debit_amount += flt(entry.debit_amount)
		closing.credit_amount += flt(entry.credit_amount)
	
	return _dict(
		opening=opening,
		closing=closing,
		total=total
	)

def get_totaled_entries(filters,gl_entries):
	data = []
	total_values = get_totals(filters,gl_entries)
	data.append(total_values.opening)
	data += gl_entries
	data.append(total_values.total)
	data.append(total_values.closing)
	return data

	


# init opening closing values
def get_opening_closing_total_values(label):
	return _dict(
		account=label,
		debit_amount=0.0,
		credit_amount=0.0,
		balance=0.0

	)

def get_data(filters):
	data = get_gl_entries(filters)
	return data

def set_balance_in_entries(data):
	balance = 0
	for d in data:
		if not d.posting_date:
			balance = 0
		balance += d.debit_amount - d.credit_amount
		d.balance = balance
	return data

def get_conditions(filters):
	conditions = []

	if filters.get("company"):
		conditions.append("company=%(company)s")

	conditions.append("is_cancelled=0")

	return "{}".format(" and ".join(conditions)) if conditions else "" 

def get_columns():
	
	columns = [
		{
			"label": "GL Entry",
			"fieldname": "gl_entry",
			"fieldtype": "Link",
			"options": "GL Entry",
			"hidden": 1
		},
		{
			"label": "Posting Date",
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 90
		},
		{
			"label": "Account",
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 180
		},
		{
			"label": "Debit (INR)",
			"fieldname": "debit_amount",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": "Credit (INR)",
			"fieldname": "credit_amount",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": "Balance (INR)",
			"fieldname": "balance",
			"fieldtype": "Float",
			"width": 130
		},
		{
			"label": "Voucher Type",
			"fieldname": "voucher_type",
			"width": 120
		},
		{
			"label": "Voucher No",
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 180
		},
		{
			"label": "Party",
			"fieldname": "party",
			"width": 100
		}
	]
	return columns



