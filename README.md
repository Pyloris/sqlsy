# sqlsy
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
schema = {
  'id':Int('id', hook='random_int', args=[0,100]),        #hook specifies the type of data to generate
  'name':VarChar('name', hook='name'),        # here generate fake names
  'job':VarChar('job', hook='job')           # here generate fake jobs
}


# create engine instance
engine = Engine(config)

# call the method to fill in the table
engine.fill_table("table_name", schema, 100)       # give it tablename, schema of table and no of rows.

# print the table if you want
engine.print_table("table_name")

# delete all the data added to the table
engine.clear_table("table_name")

# Thats IT :)
```
