// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	delivery_note(frm){
		frappe.db.get_doc('Delivery Note',frm.doc.delivery_note)
		.then(doc => {
			frm.set_value('total_amount',doc.total_amount)
			frm.set_value('total_quantity',doc.total_quantity)
			$.each(doc.items, function (index, row) {
				console.log(row)
				var childTable = frm.add_child("items");
				childTable.item_name = row.item_name;
				childTable.item_quantity = row.item_quantity;
				childTable.item_rate = row.item_rate;
				childTable.amount = row.amount;
				frm.refresh()
			})
		})
		
	}
	
});
