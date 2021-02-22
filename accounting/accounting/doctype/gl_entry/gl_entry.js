// Copyright (c) 2021, Noah Jacob and contributors
// For license information, please see license.txt

frappe.ui.form.on('GL Entry', "onload", function (frm) {
	// refresh: function(frm) {
	frm.set_query("party", function () {
		return {
			"filters": {
				"party_type": frm.doc.party_type
			}
		}
	})
	// }
});
