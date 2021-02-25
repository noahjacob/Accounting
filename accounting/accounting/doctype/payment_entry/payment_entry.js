// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	setup(frm){
		if(frm.doc.payment_type == 'Pay'){
			frm.doc.party_type = 'Supplier'}
		else{
			frm.doc.party_type = 'Customer'

		}
		

		frm.set_query("reference_type","payment_references",function(){
			if (frm.doc.party_type == "Supplier"){
				var doctypes = ["Purchase Invoice"];
			
			}else{
				var doctypes = ["Sales Invoice"]
			}
			return{
				filters:{"name":["in",doctypes]}
			}
		})

		
	},
	payment_type(frm){
		frm.clear_table("payment_references")
		frm.refresh()
		if(frm.doc.payment_type == "Receive"){
			
			frappe.db.get_value('Company',frm.doc.company,'default_receivable_account')
			.then(doc =>{
				var account_paid_from = doc.message['default_receivable_account'];
				frm.set_value('account_paid_from',account_paid_from)
				frm.set_value('account_paid_to','')

			})	
		}else{
			frappe.db.get_value('Company',frm.doc.company,'default_payable_account')
			.then(doc =>{
				var account_paid_to = doc.message['default_payable_account'];
				frm.set_value('account_paid_to',account_paid_to)
				frm.set_value('account_paid_from','')

			})

		}
	}
	
});
