import frappe

def get_context(context):
    context.items = frappe.db.get_list('Item',fields=['item_name','image', 'standard_rate','route'])
    return context