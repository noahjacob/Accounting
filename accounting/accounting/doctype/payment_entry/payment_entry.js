// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	setup(frm) {

		if (frm.doc.payment_type == 'Pay') {
			frm.doc.party_type = 'Supplier'
		}
		else {
			frm.doc.party_type = 'Customer'

		}
		if (frm.doc.reference) {
			var child = frm.add_child("payment_references")
			var invoice_type = (frm.doc.payment_type == 'Receive') ? 'Sales Invoice' : 'Purchase Invoice';




			child.reference_type = invoice_type
			child.reference_name = frm.doc.reference

			frappe.db.get_value(invoice_type, frm.doc.reference, 'total_amount').then(amount => {
				child.amount = amount.message.total_amount
				frm.doc.amount_paid = amount.message.total_amount
				console.log(child.amount)
				frm.refresh()
			})



		}
		if (frm.doc.payment_type == 'Pay') {
			frappe.db.get_value('Company', frm.doc.company, ['default_payable_account', 'default_cash_account'])
				.then(doc => {
					var account_paid_to = doc.message['default_payable_account'];
					var account_paid_from = doc.message['default_cash_account'];
					frm.set_value('account_paid_to', account_paid_to)
					frm.set_value('account_paid_from', account_paid_from)

				})

		} else {
			frappe.db.get_value('Company', frm.doc.company, ['default_receivable_account', 'default_cash_account'])
				.then(doc => {
					var account_paid_from = doc.message['default_receivable_account'];
					var account_paid_to = doc.message['default_cash_account'];
					frm.set_value('account_paid_from', account_paid_from)
					frm.set_value('account_paid_to', account_paid_to)

				})

		}


		frm.set_query("reference_type", "payment_references", function () {
			if (frm.doc.party_type == "Supplier") {
				var doctypes = ["Purchase Invoice"];

			} else {
				var doctypes = ["Sales Invoice"]
			}
			return {
				filters: { "name": ["in", doctypes] }
			}
		}),
		frm.set_query("reference_name", "payment_references", function () {
			
			
			return {
				filters: { "company": frm.doc.company }
			}
		})



	},

	refresh(frm) {
		var total_amount = 0
		$.each(frm.doc.payment_references, function (i, row) {
			total_amount = total_amount + row.amount


		})
		frm.doc.amount_paid = parseFloat(total_amount)

		if (frm.doc.payment_type == 'Pay') {

			frappe.db.get_value('Company', frm.doc.company, ['default_payable_account', 'default_cash_account'])
				.then(doc => {
					var account_paid_to = doc.message['default_payable_account'];
					var account_paid_from = doc.message['default_cash_account'];
					frm.set_value('account_paid_to', account_paid_to)
					frm.set_value('account_paid_from', account_paid_from)


				})

		} else {


			frappe.db.get_value('Company', frm.doc.company, ['default_receivable_account', 'default_cash_account'])
				.then(doc => {
					var account_paid_from = doc.message['default_receivable_account'];
					var account_paid_to = doc.message['default_cash_account'];
					frm.set_value('account_paid_from', account_paid_from)
					frm.set_value('account_paid_to', account_paid_to)

				})

		}

	},
	company(frm){
		frm.refresh()
	},
	 payment_type(frm) {
		if (frm.doc.payment_type == "Pay") {
			frm.doc.party_type = "Supplier"

		} else {
			frm.doc.party_type = "Customer"

		}
		frm.refresh()
	}, party_type(frm) {

		frm.refresh()
	}


});
frappe.ui.form.on('Payment Entry Reference', {


	amount(frm, cdt, cdn) {

		var total_amount = 0
		$.each(frm.doc.payment_references, function (i, row) {
			total_amount = total_amount + row.amount

		})
		frm.doc.amount_paid = total_amount
		frm.refresh()

	},
	payment_references_remove(frm) {
		var total_amount = 0
		$.each(frm.doc.payment_references, function (i, row) {
			total_amount = total_amount + row.amount

		})
		frm.doc.amount_paid = total_amount
		frm.refresh()
	},

})
