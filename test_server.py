
import time
import os
import datetime
from zipfile import ZipFile
import json
from flask import Flask, request, flash, redirect, render_template, session, url_for, session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd()+"/UPLOAD_FOLDER"
ALLOWED_EXTENSIONS = set(['zip'])

application = Flask(__name__)
application.secret_key = 'some_secret'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def traverse_zip(filename):
	filename = os.getcwd() + '\\' + filename
	with ZipFile(filename, 'r') as zip:
		print(zip.namelist())
		print(type(zip))
		to_json(zip.namelist())


def to_json(path_list):
    for i in range(len(path_list)):
        path_list[i] = {"path":path_list[i]} 
    json_file = open("paths.json", 'w')
    json.dump({"files":path_list},json_file)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/', methods=['GET', 'POST'])
def upload_file():		
	if request.method == 'GET':
		return render_template("sneakserv.html")

	if request.method == 'POST':
		print("Uploading a file..")
		# check if the post request has the file part
		if 'file' not in request.files:
			flash("No file was selected for upload.")
			return render_template("sneakserv.html")
		
		file = request.files['file']

		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash("File name is blank.")		
			return render_template("sneakserv.html")

		if file and allowed_file(file.filename):
			flash("Uploading: ", file.filename)
			filename = secure_filename(file.filename)
			file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
			traverse_zip(file.filename)
			return render_template("sneakserv.html")
		else:
			flash("File type not supported!")

	return render_template("sneakserv.html")

	

if __name__ == '__main__':	

	application.run(debug=True)





