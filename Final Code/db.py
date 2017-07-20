import MySQLdb

##### AUTO SUGGESTION FUNCTIONALITIES#####


### Get room id suggestions from the database "pythonTest", table "rooms" with attributes("roomID")
def get_rooms():
	# Open database connection with username= "root", password= "password" and database= "pythonTest"
	db = MySQLdb.connect("localhost","root","password","pythonTest")

	# Prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Execute SQL query using execute() method.
	# Table: rooms with attributes "roomID"
	cursor.execute("SELECT roomID FROM rooms")

	# Fetch a single row using fetchone() method.
	data = cursor.fetchall()
	res = list(sum(data, ()))
	print (data)
	print(res)

	# Disconnect from server
	db.close()
	return res

### Get login name suggestions from the database "pythonTest", table "user" with attributes("name")
def get_logins():

	# Open database connection
	db = MySQLdb.connect("localhost","root","password","pythonTest" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("SELECT name FROM user")

	# Fetch a single row using fetchone() method.
	data = cursor.fetchall()
	res = list(sum(data, ()))
	print (data)
	print(res)

	# Disconnect from server
	db.close()
	return res
