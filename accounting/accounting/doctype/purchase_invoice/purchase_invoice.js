// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	purchase_receipt(frm){
		
		frappe.call({
			method: 'accounting.accounting.doctype.purchase_invoice.purchase_invoice.get_purchase_receipt_items',
			args : {
				name: frm.doc.purchase_receipt

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
		

		
	}
	
});
frappe.ui.form.on('Purchase Invoice',{
	refresh(frm){
		if(frm.doc.docstatus){
		frm.add_custom_button(__('Make Payment'),function(){
			var i_map = {
				

			}
			frappe.new_doc('Payment Entry')
		})
		}	
	}
})
