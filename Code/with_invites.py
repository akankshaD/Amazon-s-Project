# -*- coding: utf-8 -*-

'''
This code sends meeting invites to the interviewers
Use test_data4.json
'''

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import json
import datetime
import time
import os

### Date Utilities
### Convert timestamp string to datetime object
def date_str_to_date_obj(date_str):
	return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')

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
	return time.strftime('%Y-%m-%d %H:%M', time.localtime(epoch))


def send_invites(matched_list):
	CRLF = "\r\n"
	login = "archana.r@iiitb.org"
	password = "<enterpwdhere>"
	organizer = "ORGANIZER;CN=Archana:mailto:archana.r"+CRLF+" @iiitb.org"
	fro = "Archana <archana.r@iiitb.org>"


	#utc_hrs = datetime.timedelta(hours = 5)
	utc_mins = datetime.timedelta(minutes = 330)

	for match in matched_list:
		print(match)
		start_time = datetime.datetime.strptime(match["start_time"], '%Y-%m-%d %H:%M')
		start_time = start_time - utc_mins
		end_time = datetime.datetime.strptime(match["end_time"], '%Y-%m-%d %H:%M')
		end_time = end_time - utc_mins
		room = match["room"]
		interviewer = match["login_name"]
		attendees = []
		attendees.append(interviewer)

		dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
		dtstart = start_time.strftime("%Y%m%dT%H%M%SZ")
		
		dtend = end_time.strftime("%Y%m%dT%H%M%SZ")
		
		'''
		print(dtstamp)
		print(dtstart)
		print(dtend)
		'''
		description = "DESCRIPTION: Test Meeting invitation"+CRLF
		
		attendee = "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+interviewer+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+interviewer+CRLF
		ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
		ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
		ical+= "UID:FIXMEUID"+dtstamp+CRLF
		ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
		ical+= "SUMMARY:Meeting in " + room +" on "+start_time.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF



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
		mailServer.sendmail(fro, attendees, msg.as_string())
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

# Reading data from JSON input file
with open('/home/ramesh/iiitb/amazon_project/test_data4.json') as data_file:
	data = json.load(data_file)


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
while(slot_index<len(final_slots) and room_index<len(final_rooms)):
	slot = final_slots[slot_index]
	room = final_rooms[room_index]
	if(slot["end_time"] <= room["end_time"] and slot["start_time"] >= room["start_time"]):
		# match occured
		start_time = epoch_to_date(slot["start_time"])
		end_time = epoch_to_date(slot["end_time"])
		match = {"login_name" : slot["login_name"], "room" : room["room"], "start_time" : start_time, "end_time" :  end_time}
		final_matched_list.append(match)
		countInterviews += 1

		# adjust room timings in final rooms , i.e update start time of final_rooms[room_index] to end time of slot
		room["start_time"] = slot["end_time"]

		# if start and end are same , move the room index
		if(room["start_time"] == room["end_time"]):
			room_index = room_index + 1

		# move slot index
		slot_index = slot_index + 1


	# no match occured, move the indices accordingly 
	# 3 cases here
	# 1. Increment both indices 
	# 2. Increment only room index
	# 3. Increment only slot index

	elif(slot["end_time"] > room["end_time"] and slot["start_time"] < room["start_time"]):
		room_index = room_index + 1
		slot_index = slot_index + 1


	elif(slot["end_time"] > room["end_time"] ) :
		room_index = room_index + 1

	elif(slot["start_time"] < room["start_time"]) :
		slot_index = slot_index + 1



print(countInterviews)
'''for match in final_matched_list:
	print(match)
'''
# Send invites to matched interviers
send_invites(final_matched_list)