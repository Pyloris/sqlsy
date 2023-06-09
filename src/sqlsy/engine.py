##### 
# This file contains the Engine class
# Which is responsible parsing the schema and calling the mapped functions (mappings.py)
#####


import mysql.connector
from termcolor import cprint, colored
from rich.progress import track
from rich.console import Console
from rich.table import Table
from sys import exit


class Engine:

	# current column being filled
	current_col = ""

	def __init__(self, config: dir):
		self.config = config
		self.conn = self.connect_db()
		self.cursor = self.conn.cursor()
		

	# connect to the database
	def connect_db(self):
		try:
			conn = mysql.connector.connect(**self.config)
			cprint("[+] Connection Success ", "green")
			return conn
		except mysql.connector.Error as err:
			cprint("[x] Error : {}".format(err), "red")
			exit(1)


	# fetch data
	def fetch(self, tb_name: str, cols:list):
		query = f'select {",".join(cols)} from {tb_name}'
		self.cursor.execute(query)
		return self.cursor.fetchall()


	# Create a database
	def create_db(self, db_name:str):

		try:
			cprint(f"[+] Creating Database {db_name}..", "blue")
			self.cursor.execute(f"create database {db_name};")
			self.conn.commit()

			cprint(f"[+] Database created", "green")
			self.cursor.execute("use {}".format(db_name))
			cprint(f"[+] Now using this database..", 'blue')
		except (mysql.connector.Error, Exception) as err:
			cprint("[x] Error: {}".format(err), "red")
			exit(1)



	# create tables to fill later
	def create_table(self, tb_name:str, schema:dir):
		try:
			query = "create table {} (".format(tb_name)

			for col in schema.keys():
				# check if constraints are given
				constraint = schema[col]['constraints']

				# if not, give a null str as constraint
				if not constraint:
					constraint = [""]

				# generate the table attribute
				attribute = " {} {} ".format(col, schema[col]['type'])+" ".join(constraint)+","
				query+=attribute

			# remove the last ',' from the query
			query = query[:-1]+");"

			# create the table
			self.cursor.execute(query)

			cprint(f"[+] Table {query.split()[2]} created", 'blue')
			self.conn.commit()
		except mysql.connector.Error as err:
			cprint("[x] Error: {}".format(err), 'red')
			exit(1)


	# drop the database
	def drop_db(self, db_name):
		try:
			self.cursor.execute("drop database if exists {}".format(db_name))
			self.conn.commit()
			cprint("[+] Dropped {} database".format(db_name), 'blue')
		except mysql.connector.Error as err:
			cprint("[x] Error : {}".format(err))
			exit(1)

	# drop the table
	def drop_table(self, tb_name):
		try:
			self.cursor.execute("drop table if exists {}".format(tb_name))
			self.conn.commit()
			cprint("[+] Dropped Table {}".format(tb_name), 'blue')
		except mysql.connector.Error as err:
			cprint("[+] Error : {}".format(err))
			exit(1)


	# Method to parse the schema and generate insert query
	def parse_schema(self, schema:dict, tb_name:str):
		cols = "("+','.join(schema.keys())+")"
		vals = ""

		query_holders = []
		# store for printing the table
		self.cols = schema.keys()

		for data in schema.values():

			if data['type'] == 'int':
				query_holders.append("%d")
			elif data['type'] == 'float':
				query_holders.append("%f")
			else:
				query_holders.append('"%s"')

		# build the query
		vals += "("+",".join(query_holders)+");"

		# final query
		query = f"INSERT INTO {tb_name} "+cols+" values "+vals

		return query

	
	# set current_col state
	@classmethod
	def set_col(cls, col):
		cls.current_col = col

	# get current col
	@classmethod
	def get_col(cls):
		return cls.current_col


	# method to fill the table
	def fill_table(self, table_name:str, schema:dict, n: int):

		# parse the scheme and get the query
		query = self.parse_schema(schema, table_name)

		# store generated data for insertion into table
		data = []

		for i in track(range(n), description=colored(f"[+] Working on {table_name}: ", 'blue')):
			data.clear()
			try:
				for col,attr in zip(schema.keys(),schema.values()):
					self.set_col(col)
					if 'custom_flag' in attr.keys():
						data.append(next(attr['callback']))
					elif attr['args'] == None:
						data.append(attr['callback']())
					else:
						# pass the arguments in
						data.append(attr['callback'](*attr['args']))
			except StopIteration:
				cprint("[x] The custom function generated less data then target rows!", "red")
				self.clear_table(table_name)
				exit(0)
			try:
				# add the data
				self.cursor.execute(query % tuple(data))

				# commit the data
				self.conn.commit()
			except mysql.connector.Error as err:
				cprint("[x] Error : {}".format(err), "red")
				exit(1)
			except Exception as err:
				self.clear_table(table_name)
				cprint("[x] Error: {}".format(err), 'red')
				exit(1)



	# delete everything from the database
	def clear_table(self, table_name):

		cprint("[+] Clearing the table ...", 'blue')

		self.cursor.execute(f"delete from {table_name};")
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

	def close(self):
		try:
			self.conn.close()
			cprint("[+] Closed the Connection to database", "green")
		except mysql.connector.Error as err:
			cprint('[x] Couldnt close the connection : {}'.format(err), "red")


	def __del__(self):
		try:
			if self.conn.is_connected():
				self.conn.close()
				cprint("[+] Closed the connection to mysql", "green")
		except mysql.connector.Error as err:	
			cprint("[x] Couldn't close connection : {}".format(err), "red")