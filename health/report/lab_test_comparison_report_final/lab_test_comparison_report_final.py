# Copyright (c) 2024, Adcomp System and contributors
# For license information, please see license.txt

from datetime import datetime,date

import frappe


def execute(filters=None):
	
	columns, result = get_columns(filters), get_data(filters)
	
	return columns, result


def get_columns(filters):

	columns = []
	
	fixed_columns = [

		{
			"label": "Test Parameter",
			"fieldname":"test_name",
			"fieldtype":"Data",
			"width": 250
		},

		{
			"label": "Normal Range",
			"fieldname":"normal_range",
			"fieldtype":"Data",
			"width": 250
		},

		
		
	]

	columns.extend(fixed_columns)

	result = get_data(filters)

		
	columns_lst = []

	for row in result:
		if row.get("date_str_lst"):
			columns_lst.append(row.get("date_str_lst"))
	
	columns_lst = sorted(columns_lst[0])
	columns_lst = set(columns_lst)



	for date in sorted(columns_lst):
		column = {
			"label": date,
			"fieldname": date,
			"fieldtype": "Data",
			"width": 250
		}
		columns.append(column)

	print(columns,"=========")

	return columns




def get_data(filters):

	patient = filters.get("patient")
	lab_test = filters.get("lab_test")
	start_date = filters.get("start_date")
	end_date = filters.get("end_date")


	
	
	sql_query = """
		SELECT 
			lab_test.patient AS patient,
			lab_test.status AS status,
			lab_test.date AS date,
			lab_test.template AS template,
			normarl_test.lab_test_name AS test_name,
			normarl_test.normal_range AS normal_range,
			normarl_test.result_value AS result_value
		FROM 
			`tabLab Test` AS lab_test 
		LEFT JOIN 
			`tabNormal Test Result` AS normarl_test ON lab_test.name = normarl_test.parent
	"""

	# Constructing the WHERE clause based on filters
	where_clause = []
	where_clause.append("lab_test.status = 'Completed'")
	if start_date and end_date:
		where_clause.append(f"lab_test.date BETWEEN '{start_date}' AND '{end_date}'")

	if patient:
		where_clause.append(f"lab_test.patient LIKE '%{patient}%'")

	if lab_test:
		where_clause.append(f"lab_test.template LIKE '%{lab_test}%'")
	
	# If any filters are provided, add WHERE clause to SQL query
	if where_clause:
		sql_query += " WHERE " + " AND ".join(where_clause)
	
	sql_query += ";"
	
	result = frappe.db.sql(sql_query, as_dict=True)
	

	
	date_str_lst = []
	aggregated_data = {}
	for entry in result:
		key = (entry['patient'], entry['template'], entry['test_name'], entry['normal_range'])
		
		entry["date_str_lst"] = date_str_lst
		date = entry.get("date")
		if date:
			date_str =date.strftime('%d-%m-%Y')
			date_str_lst.append(date_str)
			if key not in aggregated_data:
				aggregated_data[key] = entry
				aggregated_data[key][entry['date'].strftime('%d-%m-%Y')] = entry['result_value']
				aggregated_data[key][date_str] = entry['result_value']
				entry["date_str_lst"] = date_str_lst
			else:
				aggregated_data[key][entry['date'].strftime('%d-%m-%Y')] = entry['result_value']
				aggregated_data[key][date_str] = entry['result_value']
				entry["date_str_lst"] = date_str_lst


	# Convert aggregated data back to list of dictionaries
	result = list(aggregated_data.values())

	




	
	


	return result









	
	
	
  
	





	










	


	
