import frappe


def get_context(context):
	user = frappe.session.user
	context.user=user
	si = get_cart(user)
	context.cart = si
	return context

def get_cart(user):
	check = frappe.db.get_list('Sales Invoice',filters = {'docstatus':0,'customer':user},ignore_permissions = True)
	if check:
		si = frappe.get_doc('Sales Invoice',check[0]['name'])
		return si
	else:
		return 0
