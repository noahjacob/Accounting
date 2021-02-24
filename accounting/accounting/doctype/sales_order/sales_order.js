// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt


frappe.ui.form.on('Sales Order', {
	onload(frm) {
		frm.set_query("customer", function () {
			return {
				"filters": {
					"party_type": 'Customer'
				}
			}
		})

	},

});
frappe.ui.form.on('Sales Order Item', {
	item_quantity(frm, cdt, cdn) {
		let row = locals[cdt][cdn]

		let rate = row.item_rate;
		let qty = row.item_quantity;
		let amount = rate * qty;
		row.amount = amount;
		frm.refresh();
	},
	item_name(frm, cdt, cdn) {
		let row = locals[cdt][cdn]

		let rate = row.item_rate;
		row.item_quantity = 1;
		let qty = row.item_quantity;
		let amount = rate * qty;
		row.amount = amount;
		frm.refresh();
	},
	item_rate(frm,cdt,cdn){
		let row = locals[cdt][cdn]

		let rate = row.item_rate;
		let qty = row.item_quantity;
		let amount = rate * qty;
		row.amount = amount;
		frm.refresh();
	}
})