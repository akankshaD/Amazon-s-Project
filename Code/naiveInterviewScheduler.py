import json
from datetime import datetime

### Date Utilities
### Convert timestamp string to datetime object
def date_str_to_date_obj(date_str):
	return datetime.strptime(date_str, '%Y-%m-%d %H:%M')

### Convert datetime object to epoch seconds
def date_obj_to_epoch(date_obj):
	epoch = datetime(1970, 1, 1)
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


### Sort the list based on sort_on as key
def sort_list(sort_on, list):
	ordered_list = [(item[sort_on], item) for item in list]
	ordered_list.sort()
	final_list = [item for (key, item) in ordered_list]
	return final_list

# Reading data from JSON input file
with open('/home/akanksha/Desktop/Amazon Project/Test Data/test_data_1.json') as data_file:
	data = json.load(data_file)

### Loading data
interview_rooms = data["interview_rooms"]
#print(interview_rooms)

### Converting the start_time and end_time timestamps to epoch seconds

interview_rooms = convert_list_in_epoch_seconds(interview_rooms)
#print(interview_rooms)

### Maintaining a sorted list of interview_rooms based on end_time
final_rooms = sort_list("end_time", interview_rooms)
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
for slot in final_slots:
	for room in final_rooms:
		if((slot["end_time"] <= room["end_time"]) and (slot["start_time"] >= room["start_time"])):
			match = {"login_name" : slot["login_name"], "room" : room["room"], "start_time" : room["start_time"], "end_time" :  room["end_time"]}
			final_matched_list.append(match)
			countInterviews += 1

print(countInterviews)
for match in final_matched_list:
	print(match)


