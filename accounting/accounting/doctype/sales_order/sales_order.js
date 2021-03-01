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
	refresh(frm){
		if(frm.doc.docstatus){
		frm.add_custom_button(__('Delivery Note'),function(){
			var d_map = {
				customer:frm.doc.customer,
				sales_order:frm.doc.name,
				total_amount:parseFloat(frm.doc.total_amount),
				total_cost_price:(frm.doc.total_cost_price)
			}
			frappe.new_doc('Delivery Note',d_map)
		},__("Create"))}
		
	}

});

frappe.ui.form.on('Sales Order Item', {
	item_quantity(frm, cdt, cdn) {
		let row = locals[cdt][cdn]

		let rate = row.item_rate;
		let qty = row.item_quantity;
		let amount = rate * qty;
		row.amount = amount;
		calculate_total(frm)
		frm.refresh();
	},
	item_name(frm, cdt, cdn) {
		let row = locals[cdt][cdn]

		let rate = row.item_rate;
		row.item_quantity = 1;
		let qty = row.item_quantity;
		let amount = rate * qty;
		row.amount = amount;
		calculate_total(frm)
		frm.refresh();
	},
	item_rate(frm,cdt,cdn){
		let row = locals[cdt][cdn]

		let rate = row.item_rate;
		let qty = row.item_quantity;
		let amount = rate * qty;
		row.amount = amount;
		calculate_total(frm)
		frm.refresh();
	},
	items_remove(frm){
		calculate_total(frm)
		frm.refresh()
	}
})

var calculate_total = function(frm){
	var total = 0
	var qty = 0
	var total_cost_price = 0
		var items = frm.doc.items
		for(var i in items){
			total = total+items[i].amount
			qty = qty + items[i].item_quantity
			let cost_price = items[i].item_quantity*items[i].standard_rate
			total_cost_price = total_cost_price + cost_price
		}
		frm.doc.total_amount = flt(total)
		frm.doc.total_quantity = flt(qty)
		frm.doc.total_cost_price = flt(total_cost_price)
		frm.refresh_field('total_amount')
}