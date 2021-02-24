// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Note', {
	sales_order(frm) {
		frappe.call({
			method: 'accounting.accounting.doctype.delivery_note.delivery_note.get_sales_order_items',
			args: {
				name: frm.doc.sales_order

			},
			callback: function (r) {
				var parent = r.message


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
		
		


	}
});
