// Copyright (c) 2016, Noah Jacob and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": "Company",
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("company")
		},
		{
			"fieldname":"from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label":"To Date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(),1),
			"reqd": 1,
			"width": "60px"
		},

	]
};
