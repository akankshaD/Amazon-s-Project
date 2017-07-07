from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('data_form.html')

@app.route('/handle-data', methods=["POST,GET"])
def handle_data():
    interviewer_data = request.form['interviewer_data']
    room_data = request.form['room_data']

    return render_template('send_invites.html')
    #call algo
