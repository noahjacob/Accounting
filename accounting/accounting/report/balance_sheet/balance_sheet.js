// Copyright (c) 2016, Noah Jacob and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Balance Sheet"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("company")
		},
		{
			"fieldname":"filter_based_on",
			"label": "Filter Based On",
			"fieldtype": "Select",
			"options":["Fiscal Year","Date Range"] ,
			"default": ["Fiscal Year"],
			"width": "60px",
			on_change: function(){
				let filter_based_on = frappe.query_report.get_filter_value('filter_based_on')
				frappe.query_report.toggle_filter_display('from_date',filter_based_on === 'Fiscal Year')
				frappe.query_report.toggle_filter_display('to_date',filter_based_on === 'Fiscal Year')
				frappe.query_report.toggle_filter_display('fiscal_year',filter_based_on === 'Date Range')
				
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"fiscal_year",
			"label": "Fiscal Year",
			"fieldtype": "Link",
			"options":"fiscal_year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"width": "60px"
		},
		{
			"fieldname":"from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(),-1),
			"reqd": 1,
			"hidden":1,
			"width": "60px",
		
		},
		{
			"fieldname":"to_date",
			"label":"To Date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"hidden":1,
			"width": "60px",
			
		},
		{
			"fieldname":"chart_type",
			"label":"Chart Type",
			"fieldtype": "Select",
			"default": ["Bar"],
			"reqd": 1,
			"options":['Bar','Line'],
			"width": "60px",
			
		}

	],
	"formatter": function (value, row, column, data, default_formatter) {
		if (column.fieldname == "account") {
			value = data.account;
			column.is_tree = true;
		}

		value = default_formatter(value, row, column, data);

		if (!data.parent_account) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "bold");
			if (data.warn_if_negative && data[column.fieldname] < 0) {
				$value.addClass("text-danger");
			}

			value = $value.wrap("<p></p>").parent().html();
		}

		return value;
	},
	"tree": true,
	"name_field": "account",
	"parent_field": "parent_account",
	"initial_depth": 2
};
var validate_dates = function(from,to){
	if(from > to){
		
		return 0
	}
	else{return 1}
}