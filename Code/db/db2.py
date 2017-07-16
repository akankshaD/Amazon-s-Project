#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","","pythonTest" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT name FROM user")

# Fetch a single row using fetchone() method.
data = cursor.fetchall()
res = list(sum(data, ()))
print (data)
print(res)

# disconnect from server
db.close()