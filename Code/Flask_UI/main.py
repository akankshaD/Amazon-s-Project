from flask import Flask, render_template, jsonify, request, redirect, json

app = Flask(__name__)

@app.route('/')
def index():
	author = "Interview Scheduling"
	name = "You"
	return render_template('index.html', author = author, name=name)


interviewer_list = []
@app.route('/store_data_interviewer', methods=['POST','GET'])
def store_data_interviewer():
	interviewer = {'login_name':request.form['login_name'], 'start_time':request.form['start_time'], 'end_time':request.form['end_time']}
	#print(interviewer)
	interviewer_list.append(interviewer)
	return redirect('/')

room_list = []
@app.route('/store_data_rooms', methods=['POST','GET'])
def store_data_rooms():
	room = request.form['room']
	room_slot = {'room':request.form['room'], 'start_time':request.form['start_time'], 'end_time':request.form['end_time']}
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

	# RUN ALGO HERE 
	#and RENDER OUTPUT page
	return render_template('index.html')



if __name__ == '__main__':
	app.run()
