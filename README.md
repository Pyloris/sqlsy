# sqlsy
![badge1](https://img.shields.io/static/v1?label=first%20badge&message=SQL&color=blue)
A simple Python Module to easy fill your sql tables with data.

## Install
```bash
pip install sqlsy
```

A python module to easy filling in dummy data insde mysql databases.

```python
from sqlsy.engine import Engine
from sqlsy.utils.schema import Int, VarChar      # sql datatypes to define schema

# config for mysql connection : uses mysql api inside
config = {
  'user':'username',
  'password':'pas@word',
  'host':'localhost'
}

# define the schema of the table to fill

# hook specifies what data to generate
schema = {
  'id':Int(hook='sequence', args=[0,100]),     # generates numbers 0 - 100 inclu
  'name':VarChar(hook='name'),        # here generate fake names
  'job':VarChar(hook='job')           # here generate fake jobs
}


# create engine instance
engine = Engine(config)

# create a database to store above table, if not already created
engine.create_db('employee')

# create the table with above schema
engine.create_table('person')

# call the method to fill in the table
# 101 rows as id can take values from 0 to 100 = 101
engine.fill_table("person", schema, 101)       # give it tablename, schema of table and no of rows.

# print the table if you want
engine.print_table("table_name")

# delete all the data added to the table
engine.clear_table("table_name")

# drop the database if you want to
engine.drop_db("employee")
```


# Schema Functions to specify datatypes
`Int` - means "INT" of SQL.

`Char` - means "CHAR" of SQL. By default of size 255.

`VarChar` - means "VARCHAR" of SQL. By default of size 255 # does not take size like in SQL.

`Date` - means DATE of sql, `DateTime`, `Time` and `Timestamp`


# Hooks
### Int
`random_int` : generates random integers

`random_digits` : generates random 0-9 digit.

`sequential_choice` : generates sequenctial numbers from the range given using `args`.

```python
schema = {
  'id':Int(hook='sequential_choice', args=[50,100])
}
```

`random_choice` : Randomly chooses values from a given list
```python
schema = {
  'stream':VarChar(hook='random_choice', args=[['bca', 'btech', 'commerce', 'mtech']])
}
```

### VarChar/Char
`name` : generates full names

`first_name` : generates first names

`email` : generates emails

`last_name` : generates last names

`address` : generates fake addresses

`male_name` : generates male names

`female_name` : generates female names

`job`: generates a job name

`phone_number` : generates phone numbers


### Date/DateTime/Time/Timestamp

`future_datetime` : generates a future datetime

`past_datetime` : generates a past datetime

`future_date`: generates a future date

`past_date` : generates a past date

`time` : generates time value HH:MM:SS

`date`: generates date value

`date_of_birth` : generates dob's in YYYY-MM-DD format
