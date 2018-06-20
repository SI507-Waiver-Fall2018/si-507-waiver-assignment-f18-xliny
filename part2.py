# Linying Xie umid: xly
# these should be the only imports you need
import sys
import sqlite3

# write your code here
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

# From SQLite Tutorial: http://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
def create_connection(db_file):  
	""" create a database connection to the SQLite database
		specified by the db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
 
	return None

def print_results(conn, query, title, task):
	cur = conn.cursor()
	cur.execute(query)
 
	rows = cur.fetchall()

	if task == 1:
	 	print('{}	 {}'.format(*title))
		for row in rows:
			print('{} 	 {}'.format(row[0].encode('ascii', 'ignore').decode('utf-8'), row[1].encode('ascii', 'ignore').decode('utf-8')))

 	elif task == 2:
	 	print('{}	 {}'.format(*title))
		for row in rows:
			print('{} 	 {}'.format(row[0], ' '.join([row[1].encode('ascii', 'ignore').decode('utf-8'), row[2].encode('ascii', 'ignore').decode('utf-8')])))

 	elif task == 3:
	 	print('{}'.format(*title))
		for row in rows:
			print('{}'.format(row[0].encode('ascii', 'ignore').decode('utf-8')))

if __name__=="__main__":
	conn = create_connection('Northwind_small.sqlite')
	if sys.argv[1] == 'customers':
		query_customer = """SELECT Id, ContactName FROM Customer"""
		customer_title = ['ID', 'Customer Name']
		print_results(conn, query_customer, customer_title, 1)

	if sys.argv[1] == 'employees':
		query_employees = """SELECT Id, FirstName, LastName FROM Employee"""
		employees_title = ['ID', 'Employee Name']
		print_results(conn, query_employees, employees_title, 2)

	if sys.argv[1] == 'orders':
		if sys.argv[2][:4] == 'cust':
			query_customer_orders = """SELECT OrderDate FROM 'Order' WHERE CustomerId == '%s'""" % sys.argv[2][5:]
			customer_orders_title = ['Order Dates']
			print_results(conn, query_customer_orders, customer_orders_title, 3)
		elif sys.argv[2][:3] == 'emp':
			query_customer_orders = """SELECT o.OrderDate FROM 'Order' AS o INNER JOIN 'Employee' AS e ON o.EmployeeId = e.Id AND e.LastName = '%s'""" % sys.argv[2][4:]
			customer_orders_title = ['Order Dates']
			print_results(conn, query_customer_orders, customer_orders_title, 3)

