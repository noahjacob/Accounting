// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Receipt', {
	setup(frm){

		frm.set_query("supplier", function () {
			return {
				"filters": {
					"party_type": 'Supplier'
				}
			}
		})
	},
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
					calculate_total(frm)
					frm.refresh()
					
				})
			}
		})
		
		
		
		
		
	},
	

});
frappe.ui.form.on('Purchase Receipt',{
	refresh(frm){
		if(frm.doc.docstatus){
		frm.add_custom_button(__('Purchase Invoice'),function(){
			var r_map = {
				supplier:frm.doc.supplier,
				purchase_receipt:frm.doc.name
			}
			frappe.new_doc('Purchase Invoice',r_map)
		},__("Create"))
		}	
	}
})
frappe.ui.form.on('Purchase Receipt Item',{
	item_name(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		row.item_quantity = 1
		row.amount = row.item_quantity * row.item_rate
		calculate_total(frm)
		frm.refresh()
	},
	item_quantity(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		row.amount = row.item_quantity * row.item_rate
		calculate_total(frm)
		frm.refresh()
	},
	item_rate(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		row.amount = row.item_quantity * row.item_rate
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


