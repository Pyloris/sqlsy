# sqlsy
![badge1](https://img.shields.io/static/v1?label=python%203&message=SQL&color=blue)
![badge2](https://img.shields.io/static/v1?label=easy&message=install&color=green)

A simple Python Module to easy fill your sql tables with data.

## Install
```bash
pip install sqlsy
```

A python module to easy filling in dummy data insde mysql databases.

```python
from sqlsy import Engine
from sqlsy import Int, VarChar      # sql datatypes to define schema

# config for mysql connection : uses mysql api inside
config = {
  'user':'username',
  'password':'pas@word',
  'host':'localhost'
}

# define the schema of the table to fill

# hook specifies what data to generate
schema = {
  'id':Int(hook='sequence', args=[0,30]),     # generates numbers 0 - 30 including 30
  'name':VarChar(hook='name'),        # here generate fake names
  'job':VarChar(hook='job')           # here generate fake jobs
}


# create engine instance
engine = Engine(config)

# create a database to store above table, if not already created
engine.create_db('employee')

# create the table with above schema
engine.create_table('person', schema)

# call the method to fill in the table
# 101 rows as id can take values from 0 to 30 = 31
engine.fill_table("person", schema, 31)       # give it tablename, schema of table and no of rows.

# print the table if you want
engine.print_table("table_name")

# delete all the data added to the table
engine.clear_table("table_name")

# drop the database if you want to
engine.drop_db("employee")
```

![image](https://user-images.githubusercontent.com/76217003/230254219-aafe049f-93cd-45ff-ab97-22d960785add.png)


# Schema Functions to specify datatypes
`Int` - means "INT" of SQL.

`Float` - means "Float" of SQL. Doesnt support size and pricision as recommended by the Mysql docs.

`Char` - means "CHAR" of SQL. By default of size 255.

`VarChar` - means "VARCHAR" of SQL. By default of size 255 # does not take size like in SQL.

`Date` - means DATE of sql, `DateTime`, `Time` and `Timestamp`


# Hooks
### Int/Float
`random_int` : generates random integers - provide range with arguments
```python
tb_name = {
  'age':Int(hook='random_int', args=[10,50])
}
```

`random_digits` : generates random 0-9 digit.

`random_float` : generates random float value in the range given in args.

```python
schema = {
  'id':Float(hook='random_float', args=[50,200])
}
```

`sequence` : generates sequenctial numbers from the range given using `args`.

```python
schema = {
  'id':Int(hook='sequence', args=[50,100])
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
