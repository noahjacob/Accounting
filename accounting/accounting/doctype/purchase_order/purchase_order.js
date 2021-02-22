// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Order Item','item_quantity',function(frm, cdt,cdn) {

	let row = locals[cdt][cdn]

	let rate = row.item_rate;
	let qty  = row.item_quantity;
	let amount = rate * qty;
	row.amount = amount;
	frm.refresh();
	
});
frappe.ui.form.on('Purchase Order Item','item_name',function(frm, cdt,cdn) {

	let row = locals[cdt][cdn]

	let rate = row.item_rate;
	row.item_quantity = 1
	let qty  = row.item_quantity;
	let amount = rate * qty;
	row.amount = amount;
	frm.refresh();
	
});
frappe.ui.form.on('Purchase Order', 'onload', function (frm) {
	// refresh: function(frm) {
	frm.set_query("supplier", function () {
		return {
			"filters": {
				"party_type": 'Supplier'
			}
		}
	})
	// }
});


