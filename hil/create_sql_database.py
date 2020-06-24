# Create and populate a sql database using python

# import modules
import sqlite3
import os
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine

# set working directory
os.chdir('/Users/a.a.gonzalez.paje/Box Sync/Alberto/rapid_intel/3.0/code')

# create database and a table
data_base = sqlite3.connect("database.db")

# uncomment the following line in case you want to create a dummy table
#db.execute('create table person (firstname text, secondname text, age int)')


print os.getcwd()


# Import data (CSV format)
input_data = pd.read_csv("data/diamonds.csv")

# print file headers
input_data.head(3)

# Save dataframe into db
# Create your connection.
cnx = sqlite3.connect(':memory:')

# save data into db
sql.write_frame(input_data, name='diamonds', con=cnx)

# Get the dataframe back from the db
p2 = sql.read_frame('select * from diamonds', cnx)

pd.head(p2)

