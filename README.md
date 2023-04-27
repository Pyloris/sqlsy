# sqlsy
![badge4](https://img.shields.io/badge/MIT-License-red)
![badge3](https://img.shields.io/badge/version-v1.0.0-magenta)
![badge1](https://img.shields.io/static/v1?label=python%203&message=SQL&color=blue)
![badge2](https://img.shields.io/static/v1?label=easy&message=install&color=green)

A simple Python Module to easy fill your sql tables with data.

## Install
```bash
pip install sqlsy
```

## Quick Usage
A simple script to fill in data inside of a mysql table

```python
from sqlsy import Engine
from sqlsy import Int, VarChar      # sql datatypes to define schema

# config for mysql connection : uses mysql api inside
config = {
  'user':'username',
  'password':'pas@word',
  'host':'localhost',
  'database':'dbName'   # database to use: optional as it can be selected using a method
}

# custom function should be a generator
def get_id(n1, n2):
  i = n1
  while i < n2:
    yield i
    i += 1

# define the schema of the table to fill
# hook specifies what data to generate
schema = {
  'id':Int(custom_func=get_id(0,30)),     # generates numbers 0 - 30 including 30
  'name':VarChar(hook='name'),        # here generate fake names
  'ph_number':VarChar(hook='phone_number')           # here generate fake jobs
}


# create engine instance
engine = Engine(config)

# ASSUMING that the table is already created
# call the method to fill in the table
# 101 rows as id can take values from 0 to 30 = 31
engine.fill_table("person", schema, 31)       # give it tablename, schema of table and no of rows.

# print the table if you want
engine.print_table("table_name")

# close the connection
engine.close()
```

## API provided by Engine Class
The API include following methods and attributes:
Let the `engine` be an instance of `Engine` class
```python
engine = Engine(config)
```
### Attributes
- `engine.config` : Stores the provided config for mysql api connection
- `engine.conn` : It is what stores the connection object after connection is opened.
- `engine.cursor` : It stores the cursor to execute queries on the database.

## Methods
- `engine.fetch(table_name, [col_name1, col_name2])` : Grab the data from the specified columns directly

- `engine.create_db(database_name)` : Creates a database with name as provided in argument.

- `engine.create_table(table_name, schema)` : Creates a table with the specified Schema.

- `engine.drop_db(db_name)` : Drops the database if it exists

- `engine.drop_table(tb_name)` : Drops the table if it exists

- `engine.fill_table(tb_name, tb_schema, n_rows)` : Fills the table with tb_name as name and tb_schema as schema with n_rows of data. Make sure the provided hooks or custom_functions generate equal to or more than n_rows of data.

- `engine.print_table(tb_name)` : It prints the table in pretty format for you to see.

- `engine.clear_table(tb_name)` : It removes all the data from the table with provided table name

- `engine.close()` : It closes the connection to the database. If not called, the connection will be closed when `engine` object is destroyed.

# Schema Functions to specify datatypes

### How to Describe Schema
> Schema can be describe by using the provided functions which are documented below:

1. `Int` - means "INT" of SQL.

2. `Float` - means "Float" of SQL. Doesnt support size and pricision as recommended by the Mysql docs.

3. `Char` - means "CHAR" of SQL. By default of size 255.

4. `VarChar` - means "VARCHAR" of SQL. By default of size 255 # does not take size like in SQL.

### Equivalent to SQL counterparts
`Date`, `DateTime`, `Time`, `Timestamp`

# How Data is Generated
This module is designed such that the below provided hooks actually are mapped to functions which are responsible for data generation.

Below are the Hooks which can be used to generate data automatically, also Custom Generator functions can be provided which will then be called to generate data.


### Hooks for Int / Float type data
`random_int` : generates random integers - provide range with arguments
```python
# schema description
tb_name = {
  'age':Int(hook='random_int', args=(10,50))
}
```

`random_digit` : generates random 0-9 digit.

`random_float` : generates random float value in the range given in args.

```python
schema = {
  'id':Float(hook='random_float', args=(50,200))
}
```

`sequence` : generates sequenctial numbers from the range given using `args`.

```python
schema = {
  'id':Int(hook='sequence', args=(50,100))
}
```

`random_choice` : Randomly chooses values from a given list
```python
schema = {
  'stream':VarChar(hook='random_choice', args=(['bca', 'btech', 'commerce', 'mtech']))
}
```

### Hooks for VarChar / Char type data
`name` : generates full names

`first_name` : generates first names

`email` : generates emails

`last_name` : generates last names

`address` : generates fake addresses

`male_name` : generates male names

`female_name` : generates female names

`job`: generates a job name

`phone_number` : generates phone numbers

`md5` : Generates fake md5 hashes

`sha1` : Generates sha1 hashes

`uuid` : Generates UUID's


### Hooks for Date/DateTime/Time/Timestamp type data

`future_datetime` : generates a future datetime

`past_datetime` : generates a past datetime

`future_date`: generates a future date

`past_date` : generates a past date

`time` : generates time value HH:MM:SS

`date`: generates date value

`date_of_birth` : generates dob's in YYYY-MM-DD format
