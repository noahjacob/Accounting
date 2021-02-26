// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	purchase_receipt(frm) {

		frappe.call({
			method: 'accounting.accounting.doctype.purchase_invoice.purchase_invoice.get_purchase_receipt_items',
			args: {
				name: frm.doc.purchase_receipt

			},
			callback: function (r) {
				var parent = r.message


				$.each(parent, function (index, row) {
					console.log(row)
					var childTable = frm.add_child("items");
					childTable.item_name = row.item_name;
					childTable.item_quantity = row.item_quantity;
					childTable.item_rate = row.item_rate;
					childTable.amount = row.amount;
					calculate_total(frm)
					frm.refresh()

				})
			}
		})
		frm.refresh()



	}

});
frappe.ui.form.on('Purchase Invoice', {
	refresh(frm) {
		if (frm.doc.docstatus) {
			frm.add_custom_button(__('Make Payment'), function () {
				




					frappe.new_doc('Payment Entry',{
						payment_type:'Pay',
						amount_paid : frm.doc.total_amount,
						reference:frm.doc.name,
						
					})
					console.log(frm.doc.total_amount)


			})
		}
	}
})
frappe.ui.form.on('Purchase Invoice Item',{
	item_name(frm){
		calculate_total(frm)
		frm.refresh()
	},
	item_quantity(frm){
		calculate_total(frm)
		frm.refresh()
	},
	items_remove(frm){
		calculate_total(frm)
		frm.refresh()
	}
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
