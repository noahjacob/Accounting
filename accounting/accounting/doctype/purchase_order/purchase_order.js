// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Order Item','item_quantity',function(frm, cdt,cdn) {

	let row = locals[cdt][cdn]

	let rate = row.item_rate;
	let qty  = row.item_quantity;
	let amount = rate * qty;
	row.amount = amount;
	frm.refresh();
	
});
frappe.ui.form.on('Purchase Order Item','item_name',function(frm, cdt,cdn) {

	let row = locals[cdt][cdn]

	let rate = row.item_rate;
	row.item_quantity = 1;
	let qty  = row.item_quantity;
	let amount = rate * qty;
	row.amount = amount;
	frm.refresh();
	
});
frappe.ui.form.on('Purchase Order', 'onload', function (frm) {
	// refresh: function(frm) {
	frm.set_query("supplier", function () {
		return {
			"filters": {
				"party_type": 'Supplier'
			}
		}
	})
	// }
});
frappe.ui.form.on('Purchase Order',{
	refresh(frm){
		if(frm.doc.docstatus){
		frm.add_custom_button(__('Purchase Receipt'),function(){
			var o_map = {
				supplier:frm.doc.supplier,
				purchase_order:frm.doc.name
			}
			frappe.new_doc('Purchase Receipt',o_map)
		},__("Create"))}
		
	}
})


