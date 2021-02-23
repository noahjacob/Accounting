// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Receipt', {
	purchase_order(frm){
		
		frappe.call({
			method: 'accounting.accounting.doctype.purchase_receipt.purchase_receipt.get_purchase_order_items',
			args : {
				name: frm.doc.purchase_order

			},
			callback: function(r){
				var parent = r.message
				
				
				$.each(parent,function(index,row){
					console.log(row)
					var childTable = frm.add_child("items");
					childTable.item_name = row.item_name;
					childTable.item_quantity = row.item_quantity;
					childTable.item_rate = row.item_rate;
					childTable.amount = row.amount;
					frm.refresh()
					
				})
			}
		})
		frm.refresh()
		

		
	},
	refresh:function(frm){
		

	}

});
frappe.ui.form.on('Purchase Receipt Item',{

});

