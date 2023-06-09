####
# This file defines functions related to datatypes in mysql
# we define schema using these functions
####

from termcolor import cprint
from .utils.mapping import mapping


#  Sql datatypes
def datatype(func):
	def sql_dtype(hook=None, custom_func=None, args:tuple = None, constraints:list=None):

		mini_scheme = {}

		# store the args
		if args and isinstance(args, tuple):
			mini_scheme['args'] = args
		elif args:
			cprint("[x] Provide Arugments in a Tuple", 'red')
			exit(1)
		else:
			mini_scheme['args'] = args
		mini_scheme['constraints'] = constraints

		# check for data generator
		if not hook and not custom_func:
			cprint("[x] Neither Hook nor custom function is provided", "red")
			throw()

		elif custom_func:
			# set flag for custom function
			mini_scheme['custom_flag'] = True
			mini_scheme['callback'] = custom_func

		elif hook:
			mini_scheme['callback'] = mapping[hook]


		# call datatype specific function to return scheme
		return func(hook=hook, custom_func=custom_func, args=args, this=mini_scheme)

	return sql_dtype


@datatype
def Int(hook=None, custom_func=None, args:list=None, this=None):
	# used in dynamic query building
	this['type'] = 'int'
	return this


@datatype
def Float(hook=None, custom_func=None, args:list=None, this=None):
	# store the float type
	this['type'] = 'float'
	return this


@datatype
def Char(hook=None, custom_func=None, args:list=None, this=None):
	this['type'] = 'char(255)'
	return this


@datatype
def VarChar(hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'varchar(255)'
	return this


@datatype
def Date(hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'date'
	return this


@datatype
def Time(hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'time'
	return this


@datatype
def DateTime(hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'datetime'
	return this


@datatype
def Timestamp(hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'timestamp'
	return this