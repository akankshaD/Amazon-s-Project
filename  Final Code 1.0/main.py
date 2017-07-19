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
from flask import make_response
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


### Date Utilities
### Convert timestamp string to datetime object
def date_str_to_date_obj(date_str):
	return datetime.datetime.strptime(date_str, '%d-%m-%Y %H:%M')

### Convert datetime object to epoch seconds
def date_obj_to_epoch(date_obj):
	epoch = datetime.datetime(1970, 1, 1)
	val = (date_obj - epoch).total_seconds()
	return val

### Converting the start and end times in epoch seconds 
def convert_list_in_epoch_seconds(list):
    for item in list:
        start_time_obj = date_str_to_date_obj(item["start_time"])
        start_time_epoch = date_obj_to_epoch(start_time_obj)
        item["start_time"] = start_time_epoch

        end_time_obj = date_str_to_date_obj(item["end_time"])
        end_time_epoch = date_obj_to_epoch(end_time_obj)
        item["end_time"] = end_time_epoch
    return list

# Converting epoch to date
def epoch_to_date(epoch):
	return time.strftime('%d-%m-%Y %H:%M', time.localtime(epoch))


def send_invites(matched_list):
	CRLF = "\r\n"
	login = "akanksha.dwivedi@iiitb.org"
	password = "Akanksha@13"
	organizer = "ORGANIZER;CN=Akanksha:mailto:akanksha.dwivedi"+CRLF+" @iiitb.org"
	fro = "Akanksha <akanksha.dwivedi@iiitb.org>"


	#utc_hrs = datetime.timedelta(hours = 5)
	utc_mins = datetime.timedelta(minutes = 330)

	for match in matched_list:
		print(match)
		start_time = datetime.datetime.strptime(match["start_time"], '%d-%m-%Y %H:%M')
		start_time = start_time - utc_mins
		end_time = datetime.datetime.strptime(match["end_time"], '%d-%m-%Y %H:%M')
		end_time = end_time - utc_mins
		room = match["room"]
		interviewer = match["login_name"]
		attendees = []
		attendees.append(interviewer)

		dtstamp = datetime.datetime.now().strftime("%d%m%YT%H%M%SZ")
		dtstart = start_time.strftime("%d%m%YT%H%M%SZ")
		
		dtend = end_time.strftime("%d%m%YT%H%M%SZ")
		
		description = "DESCRIPTION: Test Meeting invitation"+CRLF
		
		attendee = "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+interviewer+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+interviewer+CRLF
		ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
		ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
		ical+= "UID:FIXMEUID"+dtstamp+CRLF
		ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
		ical+= "SUMMARY:Meeting in " + room +" on "+start_time.strftime("%d%m%Y @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF



		eml_body = "Test interview invite in " + room + " on " + match["start_time"]
		msg = MIMEMultipart('mixed')
		msg['Reply-To']=fro
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = "Interview invite"
		msg['From'] = fro
		msg['To'] = ",".join(attendees)

		part_email = MIMEText(eml_body,"html")
		part_cal = MIMEText(ical,'calendar;method=REQUEST')

		msgAlternative = MIMEMultipart('alternative')
		msg.attach(msgAlternative)

		ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
		ical_atch.set_payload(ical)
		Encoders.encode_base64(ical_atch)
		ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

		eml_atch = MIMEBase('text/plain','')
		Encoders.encode_base64(eml_atch)
		eml_atch.add_header('Content-Transfer-Encoding', "")

		msgAlternative.attach(part_email)
		msgAlternative.attach(part_cal)

		mailServer = smtplib.SMTP('smtp.outlook.com', 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(login, password)
		try:
			mailServer.sendmail(fro, attendees, msg.as_string())
		except(SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError) as err:
			return -1
		finally:
			mailServer.close()

# Combines continuous time slots for the same rooms
def combine_slots(interview_rooms):
	# sort based on rooms and then based on end times and then start times
	sorted_list = sorted(interview_rooms, key = lambda x: (x["room"], x["end_time"], x["start_time"]) )

	# Then combine continous slots
	combined_list = []
	#print("HERE")
	print(sorted_list)

	i = 0;
	while(i<len(sorted_list)):	
		j = i;
		k = i+1;
		#print("outer ", i, j , k)
		while(k<len(sorted_list) and sorted_list[j]["room"] == sorted_list[k]["room"] and sorted_list[j]["end_time"] == sorted_list[k]["start_time"]) :
			j = j+1
			k = k+1
			#print("inside ", j , k)

		# combine from i's start_time to j's end time
		combined_list.append({"room" : sorted_list[i]["room"], "start_time" : sorted_list[i]["start_time"], "end_time" : sorted_list[j]["end_time"]})

		# And move i to k
		i = k

	#print("COMBINED", len(combined_list))
	#print(combined_list)
	return combined_list

### Sort the list based on sort_on as key
def sort_list(sort_on, my_list) :
	sort_on2 = "start_time"
	return sorted(my_list, key = lambda x: (x[sort_on],x[sort_on2]) )

##### AUTO SUGGESTION #####
def get_rooms():
	# Open database connection
	db = MySQLdb.connect("localhost","root","password","pythonTest")

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

	# disconnect from server
	db.close()
	return res


##### FLASK APPLICATION #####
app = Flask(__name__)
app.secret_key = 'some secret'

@app.route('/')
def index():
	author = "Interview Scheduling"
	name = "You"
	return render_template('index.html', author = author, name=name)


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
	#print(interviewer)
	interviewer_list.append(interviewer)
	return redirect('/')

room_list = []
@app.route('/store_data_rooms', methods=['POST','GET'])
def store_data_rooms():
	room = request.form['autocomplete2']
	room_slot = {'room':request.form['autocomplete2'], 'start_time':request.form['start_time'], 'end_time':request.form['end_time']}
	#print(room_slot)
	room_list.append(room_slot)
	return redirect('/')


@app.route('/store_final_data', methods=['POST','GET'])
def store_final_data():
	#print(room_list)
	#print(interviewer_list)
	json_data  = {"interview_rooms": room_list, "interviewer_slots": interviewer_list}
	with open('input.json', 'w') as f:
		json.dump(json_data, f)

	with open('input.json', 'r') as f:
		data = json.load(f)

	# set the timezone 
	os.environ['TZ']='UTC'

	### Loading data
	interview_rooms = data["interview_rooms"]
	#print(interview_rooms)

	### Converting the start_time and end_time timestamps to epoch seconds

	interview_rooms = convert_list_in_epoch_seconds(interview_rooms)
	#print(interview_rooms)

	# Combining the room slots
	combined_rooms = combine_slots(interview_rooms)


	### Maintaining a sorted list of interview_rooms based on end_time
	final_rooms = sort_list("end_time", combined_rooms)
	#print(final_rooms)

	### Loading data
	interviewer_slots = data["interviewer_slots"]
	#print(interviewer_slots)

	### Converting the start_time and end_time timestamps to epoch seconds
	interviewer_slots = convert_list_in_epoch_seconds(interviewer_slots)
	#print(interviewer_slots)

	### Maintaining a sorted list of interviewer slots based on end_time
	final_slots = sort_list("end_time", interviewer_slots)
	#print(final_slots)

	### Performing the matching of rooms and slots
	countInterviews = 0
	final_matched_list = []

	slot_index = 0
	room_index = 0

	for i in range(len(final_slots)):
		slot = final_slots[i]
		for j in range(len(final_rooms)):
			room = final_rooms[j]
			if(slot["end_time"] <= room["end_time"] and slot["start_time"] >= room["start_time"]):
				# match occured..
				# remove the room entry from the rooms list
				# and interviewer too.. and break.
				start_time = epoch_to_date(slot["start_time"])
				end_time = epoch_to_date(slot["end_time"])
				match = {"login_name" : slot["login_name"], "room" : room["room"], "start_time" : start_time, "end_time" :  end_time}
				final_matched_list.append(match)
				countInterviews += 1

				room["start_time"] = slot["end_time"]
				# remove room
				if(room["start_time"] == room["end_time"]):
					final_rooms.remove(room)
				break;

	print(countInterviews)

	session['final_matched_list'] = final_matched_list
	return render_template('output.html', result = final_matched_list)

@app.route('/show_output', methods= ["POST", "GET"])
def show_output():
	final_matched_list= session.get('final_matched_list', None)
	errCode = send_invites(final_matched_list)
	result= {}
	if errCode == -1:
		result['message'] = 'Error Occurred!'
		result['button'] = 'Please Try Again'
	else:
		result['message'] = 'Invites Sent Successfully'
		result['button'] = 'Return To HomePage'
	return render_template('redirection.html', result= result)

@app.route('/go_to_home_page', methods=["POST", "GET"])
def go_to_home_page():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()
