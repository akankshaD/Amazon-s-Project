import os
import json
import date
import algo_utils

### Returns the final_matched_list of free room slots with the interviewers free slots. Take filename.json as input 
def algo(filename):

	### Open the file in read mode and load the json data
	with open(filename, 'r') as f:
		data = json.load(f)

	# set the timezone 
	os.environ['TZ']='UTC'

	### Loading data
	interview_rooms = data["interview_rooms"]

	### Converting the start_time and end_time timestamps to epoch seconds
	interview_rooms = date.convert_list_in_epoch_seconds(interview_rooms)

	# Combining the room slots
	combined_rooms = algo_utils.combine_slots(interview_rooms)


	### Maintaining a sorted list of interview_rooms based on end_time
	final_rooms = algo_utils.sort_list("end_time", combined_rooms)

	### Loading data
	interviewer_slots = data["interviewer_slots"]

	### Converting the start_time and end_time timestamps to epoch seconds
	interviewer_slots = date.convert_list_in_epoch_seconds(interviewer_slots)

	### Maintaining a sorted list of interviewer slots based on end_time
	final_slots = algo_utils.sort_list("end_time", interviewer_slots)
	

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
				start_time = date.epoch_to_date(slot["start_time"])
				end_time = date.epoch_to_date(slot["end_time"])
				match = {"login_name" : slot["login_name"], "room" : room["room"], "start_time" : start_time, "end_time" :  end_time}
				final_matched_list.append(match)
				countInterviews += 1

				room["start_time"] = slot["end_time"]
				# remove room
				if(room["start_time"] == room["end_time"]):
					final_rooms.remove(room)
				break;

	print(countInterviews)
	return final_matched_list