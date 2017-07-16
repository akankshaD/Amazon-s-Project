#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, jsonify, url_for
import random
import string
import logging
import json
from flask import make_response

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'pythonTest'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from user")
	data = cursor.fetchone()
	print(data)

	cursor.close() 
	conn.close()

	return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)