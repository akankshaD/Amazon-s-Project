from flask import Flask, render_template, request, redirect, jsonify, url_for
import random
import string
import logging
import json
import httplib2
import requests
import MySQLdb
from flask import make_response


app = Flask(__name__)


# Route to jQuery Examples
@app.route('/jQueryExamples', methods=['GET'])
def jQueryExamples():
	print "Show jQuery Examples"
	return render_template('try1.html')

def get_from_db():


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
	return res

# ** Example 1 ** 
# Autocomplete method - called from Jinja template
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
	search = request.args.get('q')

	'''results = [{'value': 'WormBase RNAi', 'label': 'WormBase RNAi'}, \
		{'value': 'Wormpep', 'label': 'Wormpep'}, {'value': 'Xenbase', 'label': 'Xenbase'}, \
		{'value': 'Resource 1', 'label': 'Resource 1'}, {'value': 'Resource 2', 'label': 'Resource 2'}, \
		{'value': 'Resource 3', 'label': 'Resource 3'}, {'value': 'Resource 4', 'label': 'Resource 4'}, \
		{'value': 'Resource 5', 'label': 'Resource 5'}, {'value': 'Resource 6', 'label': 'Resource 6'}]
	'''
	#results = [ 'Resource 1','Resource 2']
	results = get_from_db()
	return jsonify(matching_results=results)
	#results = ["car", "carriage", "horse", "dog"]
	#return jsonify(matching_results=results)

# Route to home page
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def show_home():
	return render_template('index.html')


# Main Method
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
