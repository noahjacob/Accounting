frappe.provide("frappe.treeview_settings")
frappe.treeview_settings["Account"] = {
    breadcrumb: "Accounts",
    title: __("Chart of Accounts"),
    

    filters:[
        {
            fieldname:"Company",
            fieldtype:"Link",
            options:"Company",
            label:__("Company"),
                   }
    ]

}