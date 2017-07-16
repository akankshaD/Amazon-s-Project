from flask import Flask, render_template, jsonify, request, redirect, json, Response
import json
import os.path


app = Flask(__name__)

NAMES=["abc","abcd","abcde","abcdef"]



@app.route('/autocomplete', methods=['GET'])
def autocomplete():
	search = request.args.get('q')
	query = db_session.query(Movie.title).filter(Movie.title.like('%' + str(search) + '%'))
	#results = [mv[0] for mv in query.all()]

	app.logger.debug(search)
	return jsonify(json_list=NAMES) 
    #return jsonify(matching_results=results)


if __name__ == '__main__':
	app.run()



@app.route('/',methods=['GET','POST'])
def index():
    
    return render_template("search.html")

if __name__ == '__main__':
    app.run(debug=True)