from datetime import datetime

def date_str_to_date_obj(date_str):
	return datetime.strptime(date_str, '%Y-%m-%d %H:%M')

def date_obj_to_epoch(date_obj):
	epoch = datetime(1970, 1, 1)
	val = (date_obj - epoch).total_seconds()
	return val
