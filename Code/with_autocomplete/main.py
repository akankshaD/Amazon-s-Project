from flask import Flask, render_template, jsonify, request, redirect, json,  url_for
import os.path
import random
import string
import logging
import json
import httplib2
import requests
import MySQLdb
from flask import make_response


app = Flask(__name__)

@app.route('/')
def index():
	author = "Interview Scheduling"
	name = "You"
	return render_template('input.html', author = author, name=name)

def get_rooms():
	# Open database connection
	db = MySQLdb.connect("localhost","root","","pythonTest" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("SELECT roomID FROM rooms")

	# Fetch a single row using fetchone() method.
	data = cursor.fetchall()
	res = list(sum(data, ()))
	print (data)
	print(res)

	# disconnect from server
	db.close()
	return res


def get_logins():

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


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
	search = request.args.get('q')

	
	print("inside")
	#results = [ 'Resource 1','Resource 2']
	results = get_logins()
	return jsonify(matching_results=results)


@app.route('/autocomplete2', methods=['GET'])
def autocomplete2():
	search = request.args.get('q')

	
	print("rooms auto func")
	#results = [ 'Resource 1','Resource 2']
	results = get_rooms()
	return jsonify(matching_results=results)


interviewer_list = []
@app.route('/store_data_interviewer', methods=['POST','GET'])
def store_data_interviewer():

	interviewer = {'login_name':request.form['autocomplete'], 'start_time':request.form['start_time'], 'end_time':request.form['end_time']}
	print(interviewer)
	interviewer_list.append(interviewer)
	return redirect('/')

@app.route('/store_final_data', methods=['POST','GET'])
def store_final_data():
	print(room_list)
	print(interviewer_list)
	json_data  = {"interview_rooms": room_list, "interviewer_slots": interviewer_list}
	with open('input.json', 'w') as f:
		json.dump(json_data, f)


	# RUN ALGO HERE 
	#and RENDER OUTPUT page
	return render_template('input.html')

room_list = []
@app.route('/store_data_rooms', methods=['POST','GET'])
def store_data_rooms():
	room = request.form['autocomplete2']
	room_slot = {'room':request.form['autocomplete2'], 'start_time':request.form['start_time'], 'end_time':request.form['end_time']}

	print(room_slot)

	room_list.append(room_slot)

	return redirect('/')

if __name__ == '__main__':
	app.run()