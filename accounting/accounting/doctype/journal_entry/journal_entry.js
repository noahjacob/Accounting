// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
	setup(frm){
		
		frm.set_query("account", "accounts", function () {
			return {
				"filters": {
					"company": frm.doc.company,
					"is_group":0
				}
			}

	})
}
});
frappe.ui.form.on('Journal Entry Account', {
	accounts_add(frm,cdt,cdn){
		
		let new_row = locals[cdt][cdn]
		
		
		if((frm.doc.accounts.length %2)==0) {
			$.each(frm.doc.accounts, function (index, row) {
				if(index == (frm.doc.accounts.length - 2)){
					if(row.credit){
						new_row.debit = row.credit
						frm.refresh()
					}
					else{
						new_row.credit = row.debit
						frm.refresh()
					}
				}
				
			})
			calculate_total(frm)
			
		}	
},
	accounts_remove(frm){
		calculate_total(frm)
		frm.refresh()
	},
	debit(frm){
		calculate_total(frm)
		frm.refresh()
		
	},
	credit(frm){
		calculate_total(frm)
		frm.refresh()
	}
});
var calculate_total = function(frm){
	var total_credit = 0
	var total_debit = 0
		var accounts = frm.doc.accounts
		for(var a in accounts){
			total_credit +=accounts[a].credit
			total_debit += accounts[a].debit
			
		}
		frm.doc.total_debit = flt(total_debit)
		frm.doc.total_credit = flt(total_credit)
		frm.refresh()
		
}