// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Note', {
	setup(frm){frm.set_query("customer", function () {
		return {
			"filters": {
				"party_type": 'Customer'
			}
		}
	})},
	sales_order(frm) {
		frm.clear
		frappe.call({
			method: 'accounting.accounting.doctype.delivery_note.delivery_note.get_sales_order_items',
			args: {
				name: frm.doc.sales_order

			},
			callback: function (r) {
				var parent = r.message
				frm.clear_table('items')
				frm.refresh_field('items')


				$.each(parent, function (index, row) {
					console.log(row)
					var childTable = frm.add_child("items");
					childTable.item_name = row.item_name;
					childTable.delivery_date = row.delivery_date;
					childTable.item_quantity = row.item_quantity;
					childTable.item_rate = row.item_rate;
					childTable.amount = row.amount;
					childTable.standard_rate = row.standard_rate;
					
					frm.refresh()

				})
			}
		})
		
		


	},
	refresh(frm){
		if(frm.doc.docstatus){
			frm.add_custom_button(__('Sales Invoice'),function(){
				var i_map = {
					customer:frm.doc.customer,
					delivery_note:frm.doc.name,
					total_amount:frm.doc.total_amount,
					
				}
				frappe.new_doc('Sales Invoice',i_map)
			},__("Create"))}
	}
});
frappe.ui.form.on('Delivery Note Item',{
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
	},
	
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