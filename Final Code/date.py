import datetime
import time

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