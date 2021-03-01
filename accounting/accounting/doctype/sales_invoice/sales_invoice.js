// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	delivery_note(frm){
		frm.clear_table('items')
		frappe.db.get_doc('Delivery Note',frm.doc.delivery_note)
		.then(doc => {
			$.each(doc.items, function (index, row) {
				console.log(row)
				var childTable = frm.add_child("items");
				childTable.item_name = row.item_name;
				childTable.item_quantity = row.item_quantity;
				childTable.item_rate = row.item_rate;
				childTable.amount = row.amount;
				calculate_total(frm)
				frm.refresh()
			})
		})
		
	}
	
});
frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		if (frm.doc.docstatus) {
			frm.add_custom_button(__('Make Payment'), function () {
				
					frappe.new_doc('Payment Entry',{
						payment_type:'Receive',
						amount_paid : frm.doc.total_amount,
						reference:frm.doc.name,
						
					})
					console.log(frm.doc.total_amount)


			})
		}
	}
})
frappe.ui.form.on('Sales Invoice Item',{
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
		var items = frm.doc.items
		for(var i in items){
			total = total+items[i].amount
			qty = qty + items[i].item_quantity
			
		}
		frm.doc.total_amount = flt(total)
		frm.doc.total_quantity = flt(qty)
		frm.refresh_field('total_amount')
}