import re
import time
import os
import datetime
from zipfile import ZipFile
import json
from sys import platform
from flask import Flask, request, flash, redirect, render_template, session, url_for, session, send_file, current_app, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd()+"/UPLOAD_FOLDER"
ALLOWED_EXTENSIONS = set(['zip'])

application = Flask(__name__)
application.secret_key = 'some_secret'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def traverse_zip(filename):
	filename = os.getcwd() + "/UPLOAD_FOLDER/" + filename
	with ZipFile(filename, 'r') as zip:
		print(zip.namelist())
		print(type(zip))
		to_json(zip.namelist(), filename.split('.')[0])


def to_json(path_list, root_name):
    books = []
    movies = []
    music = []
    files = []
    pics = []

    music_re = re.compile(r"((PCM)|(WAV)|(AIFF)|(MP3)|(AAC)|(OGG)|(WMA)|(FLAC))$", re.IGNORECASE)
    movie_re = re.compile(r"((AVI)|(MP4)|(WMV)|(MOV))$", re.IGNORECASE)
    books_re = re.compile(r"((DOC)|(EPUB)|(MOBI)|(AZW3?)|(IBA)|(PDF))$", re.IGNORECASE)
    pics_re = re.compile(r"((PNG)|(JPG)|(JPEG)|(GIF)|(TIF)|(BMP)|(EXIF)|(RAW)|(PPM)|(BAT)|(SVG))$", re.IGNORECASE)

    for i in range(len(path_list)):
        root_name_len = len(root_name)
        path_list[i] = '.' + path_list[i][root_name_len:]
        if music_re.search(path_list[i]):
            music.append({"path":path_list[i]})
        elif movie_re.search(path_list[i]):
            movies.append({"path":path_list[i]})
        elif books_re.search(path_list[i]):
            books.append({"path":path_list[i]})
        elif pics_re.search(path_list[i]):
            pics.append({"path":path_list[i]})
        else: 
            files.append({"path":path_list[i]})
    
    everything = dict()
    everything["all_files"] = dict()
    everything["all_files"]["music"] = music
    everything["all_files"]["movies"] = movies
    everything["all_files"]["books"] = books
    everything["all_files"]["pics"] = pics
    everything["all_files"]["files"] = files
    
    json_file = open(os.getcwd() + "/UPLOAD_FOLDER" + "/paths.js", 'w')
    json_file.write("window.jsonData=")
    json.dump(everything, json_file)
    json_file.write(';')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/download_zip', methods=['GET', 'POST'])
def download_zip():
    print("download_zip() called")
    print(session)
    filename = ""
    if 'filename' in session:
        filename = session['filename']
    return send_from_directory(directory=os.getcwd() + "/UPLOAD_FOLDER", filename=filename)



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
			session['filename'] = file.filename 
			return render_template("sneakserv.html")
		else:
			flash("File type not supported!")

	return render_template("sneakserv.html")

	

if __name__ == '__main__':	
    if not os.path.exists(os.getcwd() + "/UPLOAD_FOLDER"): 
        os.makedirs(os.getcwd() + "/UPLOAD_FOLDER")
    application.run(debug=True)





