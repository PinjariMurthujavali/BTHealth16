// Copyright (c) 2024, mj and contributors
// For license information, please see license.txt

frappe.query_reports["Lab Test Comparison Report Final"] = {
	"filters": [

		{
			"fieldname": "patient",
			"label": __("Patient"),
			"fieldtype": "Link",
			"options":"Patient",
			"reqd": 1
		},
		
		{
			"fieldname": "lab_test",
			"label": __("Lab Test"),
			"fieldtype": "Link",
			"options":"Lab Test Template",
			"reqd": 1
		},
	
		{
			"fieldname": "start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 1
			
		},

		{
			"fieldname": "end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 1
			
		},
		
	]
};
