from __future__ import unicode_literals
import frappe
from frappe.utils import now

def make_gl_entry(self,account,debit,credit,against = None):
    gl_entry = frappe.get_doc({
            'doctype':'GL Entry',
            'posting_date':self.posting_date,
            'account':account,
            'debit_amount':debit,
            'credit_amount':credit,
            'company':self.company,
            'voucher_type':self.doctype,
            'voucher_no':self.name
            
    })
    gl_entry.insert()


def make_reverse_gl_entry(self,voucher_type,voucher_no):
        gl_entries = frappe.get_all("GL Entry",
                        fields = ["*"],
                        filters = {
                                "voucher_type":voucher_type,
                                "voucher_no":voucher_no,
                                "is_cancelled":0
                        })
        
        if gl_entries:
                cancel_entries(gl_entries[0]['voucher_type'],gl_entries[0]['voucher_no'])

                for entry in gl_entries:
                        entry['name'] = None
                        debit = entry.get('debit_amount',0)
                        credit = entry.get('credit_amount',0)

                        entry['debit_amount'] = credit
                        entry['credit_amount'] = debit

                        entry['is_cancelled'] = 1

                        if entry['debit_amount'] or entry['credit_amount']:
                                make_reverse_entry(entry)

def make_reverse_entry(entry):
        gle = frappe.new_doc('GL Entry')
        gle.update(entry)
        gle.insert()
        

def cancel_entries(voucher_type,voucher_no):
        frappe.db.sql(""" UPDATE `tabGL Entry` SET is_cancelled = 1,
        modified = %s,modified_by = %s

        WHERE voucher_type = %s and voucher_no = %s and is_cancelled = 0""",
        (now(),frappe.session.user,voucher_type,voucher_no))