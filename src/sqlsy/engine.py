##### 
# This file contains the Engine class
# Which is responsible parsing the schema and calling the mapped functions (mappings.py)
#####


import mysql.connector
from termcolor import cprint, colored
from rich.progress import track
from rich.console import Console
from rich.table import Table


class Engine:

	def __init__(self, config: dir):
		self.config = config
		self.conn = self.connect_db()

		
	# connect to the database
	def connect_db(self):
		try:
			conn = mysql.connector.connect(**self.config)
			cprint("[+] Connection Success ", "green")
			return conn
		except Exception:
			cprint("[x] ERROR :: Couldn't connect to mysql server!", "red")
			exit(0)


	# fetch data
	def fetch(self, query):
		cursor = self.conn.cursor()

		cursor.execute(query)

		return cursor.fetchall()


	# Method to parse the schema and generate insert query
	def parse_schema(self, schema:dict, tb_name:str):
		cols = "("+','.join(schema.keys())+")"
		vals = ""

		query_holders = []
		self.cols = []

		for data in schema.values():
			# store for printing table
			self.cols.append(data['attr'])

			if data['type'] == 'int':
				query_holders.append("%d")
			else:
				query_holders.append("'%s'")

		# build the query
		vals += "("+','.join(query_holders)+");"

		# final query
		query = f"INSERT INTO {tb_name} "+cols+" values "+vals

		return query

	
	# method to fill the table
	def fill_table(self, table_name:str, schema:dict, n: int):
		# get cursor
		cursor = self.conn.cursor()

		# parse the scheme and get the query
		query = self.parse_schema(schema, table_name)

		# store generated data for insertion into table
		data = []

		for i in track(range(n), description=colored(f"[+] Working on {table_name}: ", 'blue')):
			data.clear()

			for attr in schema.values():
				if attr['args'] == None:
					data.append(attr['callback']())
				else:
					# pass the arguments in
					data.append(attr['callback'](*attr['args']))

			try:
				# add the data
				cursor.execute(query % tuple(data))

				# commit the data
				self.conn.commit()
			except Exception:
				cprint("[x] Data couldn't be added to the table", "red")
				return 0



	# delete everything from the database
	def clear_table(self, table_name):
		cursor = self.conn.cursor()

		cprint("[+] Clearing the table ...", 'blue')

		cursor.execute(f"delete from {table_name};")
		self.conn.commit()


	# show the table
	def print_table(self, table_name:str):
		console = Console()

		table = Table(title=table_name)

		# add columns
		for col in self.cols:
			table.add_column(col, style='magenta')

		# select the data
		cursor = self.conn.cursor()
		cursor.execute(f"select * from {table_name};")
		data = cursor.fetchall()

		for row in data:
			row = list(map(str, row))
			table.add_row(*row)

		# print the table
		console.print(table)


	def __del__(self):
		try:
			self.conn.close()
			cprint("[+] Closed the connection to mysql", "green")
		except Exception:	
			cprint("[x] Couldn't Close the connection to mysql", "red")