####
# This file defines functions related to datatypes in mysql
# we define schema using these functions
####

from termcolor import cprint
from .mapping import mapping


# decorator for Sql datatype
def datatype(func):
	def sql_dtype(attribute, *, hook=None, custom_func=None, args:list = None, this=None):

		mini_scheme = {}

		mini_scheme['attr'] = attribute

		# store the args
		mini_scheme['args'] = args

		# check for data generator
		if not hook and not custom_func:
			cprint("[x] Neither Hook nor custom function is provided", "red")
			throw()

		elif custom_func:
			mini_scheme['callback'] = custom_func

		elif hook:
			mini_scheme['callback'] = mapping[hook]


		# call datatype specific function to return scheme
		return func(attribute, hook=hook, custom_func=custom_func, args=args, this=mini_scheme)

	return sql_dtype


@datatype
def Int(attribute, *, hook=None, custom_func=None, args:list=None, this=None):
	# used in dynamic query building
	this['type'] = 'int'
	return this



@datatype
def Char(attribute, *, hook=None, custom_func=None, args:list=None, this=None):
	this['type'] = 'char'
	return this


@datatype
def VarChar(attribute, *, hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'varchar'
	return this


@datatype
def Date(attribute, *, hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'date'
	return this


@datatype
def Time(attribute, *, hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'time'
	return this


@datatype
def DateTime(attribute, *, hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'datetime'
	return this


@datatype
def Timestamp(attribute, *, hook=None, custom_func=None, args:list = None, this=None):
	this['type'] = 'timestamp'
	return this