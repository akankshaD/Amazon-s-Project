### Algorithm Utility Functions

# Combines continuous time slots for the same rooms
def combine_slots(interview_rooms):
	# sort based on rooms and then based on end times and then start times
	sorted_list = sorted(interview_rooms, key = lambda x: (x["room"], x["end_time"], x["start_time"]) )

	# Then combine continous slots
	combined_list = []

	i = 0;
	while(i<len(sorted_list)):	
		j = i;
		k = i+1;
		
		while(k<len(sorted_list) and sorted_list[j]["room"] == sorted_list[k]["room"] and sorted_list[j]["end_time"] == sorted_list[k]["start_time"]) :
			j = j+1
			k = k+1
			

		# combine from i's start_time to j's end time
		combined_list.append({"room" : sorted_list[i]["room"], "start_time" : sorted_list[i]["start_time"], "end_time" : sorted_list[j]["end_time"]})

		# And move i to k
		i = k

	
	return combined_list

### Sort the list based on sort_on as key
def sort_list(sort_on, my_list) :
	sort_on2 = "start_time"
	return sorted(my_list, key = lambda x: (x[sort_on],x[sort_on2]) )