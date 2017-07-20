from flask import Flask, render_template, jsonify, request, redirect, json,  url_for, session
import os
import random
import string
import logging
import json
import httplib2
import requests
import MySQLdb
import json
import datetime
import time
import smtplib

#### IMPORT FROM CUSTOM FILES

import date
import algo
import algo_utils
import db
import send_invites


##### FLASK APPLICATION #####

app = Flask(__name__)
app.secret_key = 'some secret'


### For the HomePage
@app.route('/')
def index():
	author = "Interview Scheduling"
	name = "IIIT-B"
	return render_template('index.html', author = author, name=name)


### For auto suggestions of login names from the database
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
	search = request.args.get('q')

	print("inside")
	#results = [ 'Resource 1','Resource 2']
	results = db.get_logins()
	return jsonify(matching_results=results)


### For auto suggestions of rooms ids from the database
@app.route('/autocomplete2', methods=['GET'])
def autocomplete2():
	search = request.args.get('q')

	print("rooms auto func")
	
	results = db.get_rooms()
	return jsonify(matching_results=results)


### For input of interviewer details
interviewer_list = []
@app.route('/store_data_interviewer', methods=['POST','GET'])
def store_data_interviewer():
	interviewer = {'login_name':request.form['autocomplete'], 'start_time':request.form['start_time'], 'end_time':request.form['end_time']}
	#print(interviewer)
	interviewer_list.append(interviewer)
	return redirect('/')


### For input to Rooms slots
room_list = []
@app.route('/store_data_rooms', methods=['POST','GET'])
def store_data_rooms():
	room = request.form['autocomplete2']
	room_slot = {'room':request.form['autocomplete2'], 'start_time':request.form['start_time'], 'end_time':request.form['end_time']}
	#print(room_slot)
	room_list.append(room_slot)
	return redirect('/')


### Storing the final room slots and interviewer slots into json file and call the algorithm
@app.route('/store_final_data', methods=['POST','GET'])
def store_final_data():
	#print(room_list)
	#print(interviewer_list)
	json_data  = {"interview_rooms": room_list, "interviewer_slots": interviewer_list}
	with open('input.json', 'w') as f:
		json.dump(json_data, f)

	final_matched_list = algo.algo('input.json')

	session['final_matched_list'] = final_matched_list
	return render_template('output.html', result = final_matched_list)


### To show the output
@app.route('/show_output', methods= ["POST", "GET"])
def show_output():
	final_matched_list= session.get('final_matched_list', None)
	errCode = send_invites.send_invites(final_matched_list)
	result= {}
	if errCode == -1:
		result['message'] = 'Error Occurred!'
		result['button'] = 'Please Try Again'
	else:
		result['message'] = 'Invites Sent Successfully'
		result['button'] = 'Return To HomePage'
	return render_template('redirection.html', result= result)


### Go to homepage from output page
@app.route('/go_to_home_page', methods=["POST", "GET"])
def go_to_home_page():
	return render_template('index.html')


if __name__ == '__main__':
	app.run()
