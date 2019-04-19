
import app_methods
import time
import datetime
from flask import Flask, request, flash, redirect, render_template, url_for, session

application = Flask(__name__)
application.secret_key = 'some_secret'
#INPUT_DATA_URL = "https://s3-us-west-2.amazonaws.com/css490/input.txt"
#INPUT_DATA_URL = "https://css490.blob.core.windows.net/lab4/input.txt"
INPUT_DATA_URL = "https://s3-us-west-2.amazonaws.com/drewlcss490/input3.txt"

@application.route('/')
def index():	
	try: 
		session['Loaded']
		session['LastClicked'] 
	except KeyError:
		session['Loaded'] = False
		session['LastClicked'] = datetime.datetime.now()
	return render_template('index.html')

@application.route('/', methods=['POST'])
def form_post():		
	print(session)
	
	if pressed_too_quickly(): 
		flash("You're pressing buttons to fast! Please wait a few seconds.")
		return redirect(url_for('index'))

	if session['Loaded'] == False: 
		flash("The data must be loaded in order to query!")
		return redirect(url_for('index'))

	FirstName = request.form['FirstName']
	LastName = request.form['LastName']	

	if FirstName == "" and LastName == "": 		
		flash("You must enter either a first name or last name to query on!")
		return redirect(url_for('index'))

	# Make query here: 
	response = False

	# QUERY CALL:
	#=========================================#
	response = app_methods.query_ddb(FirstName, LastName)
	#=========================================#
	if response == False:
		flash("The data must be loaded in order to query!")
		return redirect(url_for('index'))
	response = response['Items']
	count = str(len(response))
	
	# Convert the response into a easier to print format for Jninja:
	people = []
	for item in response:
		person = {'first_name':item['first_name'],'last_name':item['last_name']}
		del item['first_name']
		del item['last_name']
		attrs = item 
		people.append((person, attrs))
	
	# Make sure to sanitize inputs: https://blog.sqreen.com/preventing-sql-injections-in-python/
	# query may return multiple persons
	return render_template('details.html', people=people, count=count)

@application.route('/load')
def load():		
	if pressed_too_quickly(): 
		flash("You're pressing buttons to fast! Please wait a few seconds.")
		return redirect(url_for('index'))
	app_methods.load(INPUT_DATA_URL)		
	session['Loaded'] = True 
	flash("Data has been loaded.")	
	return redirect(url_for('index'))

@application.route('/clear')
def clear():
	if pressed_too_quickly(): 
		flash("You're pressing buttons to fast! Please wait a few seconds.")
		return redirect(url_for('index'))
	app_methods.clear()
	session['Loaded'] = False
	flash("Data has been cleared!")	
	return redirect(url_for('index'))

@application.route('/return_home')
def return_home():
	return redirect(url_for('index'))

def pressed_too_quickly():
	print(session)

	# Grab LastClicked 
	time_now = datetime.datetime.now()
	last_clicked = session['LastClicked']

	# Update LastClicked:
	session['LastClicked'] = time_now

	# Compare time_now and LastClicked
	difference = (time_now - last_clicked).seconds

	if difference < 2: 	return True
	else:		 		return False

if __name__ == '__main__':	

	application.run(debug=True)





