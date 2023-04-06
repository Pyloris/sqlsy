# sqlsy
### Install
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
  'host':'localhost',
  'database':'db_name'
}

# define the schema of the table to fill

# hook specifies what data to generate
schema = {
  'id':Int('id', hook='seq_choice', args=[0,100]),     # generates numbers 0 - 100 inclu
  'name':VarChar('name', hook='name'),        # here generate fake names
  'job':VarChar('job', hook='job')           # here generate fake jobs
}


# create engine instance
engine = Engine(config)

# call the method to fill in the table
# 101 rows as id can take values from 0 to 100 = 101
engine.fill_table("table_name", schema, 101)       # give it tablename, schema of table and no of rows.

# print the table if you want
engine.print_table("table_name")

# delete all the data added to the table
engine.clear_table("table_name")

# Thats IT :)
```


# Schema Functions to specify datatypes
`Int` - means "INT" of SQL.

`Char` - means "CHAR" of SQL.

`VarChar` - means "VARCHAR" of SQL. # does not take size like in SQL.

`Date` - means DATE of sql, `DateTime`, `Time` and `Timestamp`


# Hooks
### Int
`random_int` : generates random integers

`random_digits` : generates random 0-9 digit.

`seq_choice` : generates sequenctial numbers from the range given using `args`.

```python
schema = {
  'id':Int('id', hook='seq_choice', args=[50,100])
}
```

### VarChar/Char
`name` : generates full names

`first_name` : generates first names

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


### Choose randomly from a list
For example if we want to choose values from a provided list at random we can use the hook `random_choice`.
```python
schema = {
  'stream':VarChar('stream', hook='random_choice', args=[['Science', 'BCA', 'BTech']])
}
# stream will contain values from the given list in `args` at random.
```
