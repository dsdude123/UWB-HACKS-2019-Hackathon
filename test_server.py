
import time
import os
import datetime
from flask import Flask, request, flash, redirect, render_template, session, url_for, session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd()+"/UPLOAD_FOLDER"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

application = Flask(__name__)
application.secret_key = 'some_secret'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	
@application.route('/', methods=['GET', 'POST'])
def upload_file():		
	if request.method == 'GET':
		return render_template("test_html.html")


	if request.method == 'POST':
		print("GOT HERE")
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			print("No file part")
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			print("No file selected.s")
			#flash('No selected file')
			return redirect(request.url)
		if file:
			print("YO WADDUP")
			filename = secure_filename(file.filename)
			file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
			#return redirect(url_for('uploaded_file',filename=filename))
			return render_template("test_html.html")
	return '''
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form method=post enctype=multipart/form-data>
	  <input type=file name=file>
	  <input type=submit value=Upload>
	</form>
	'''

	

if __name__ == '__main__':	

	application.run(debug=True)





