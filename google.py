from flask import Flask, render_template, request, redirect,send_from_directory
from flask import flash, request, session, abort, url_for
import os
import base64
from pymongo import MongoClient
import datetime
import time

app = Flask(__name__)

#database connection
client=MongoClient('localhost',27017)
if client:
	print "WOW!! Connection established"
db=client.drash
db=client['drash']
print db
collection=db.images
collection=db['images']
print collection
#client.admin.authenticate('pateldrashti', 'cloud')
client.drash.add_user('pateldrashti', 'cloud', roles=[{'role':'readWrite','db':'drash'}])
print 'user done'
#fileLimit = 15
#sizeLimit = 1000000
comment_limit = 100
@app.route('/')
def index():
    return app.send_static_file('login.html')
	
@app.route('/login', methods=['POST'])
def do_admin_login():

	username=request.form['username']
	pwd=request.form['password']
	if username=='pateldrashti' and pwd=='cloud':
		return app.send_static_file('index.html')
	else:
		return '<h3>Invalid username/password</h3><br><form action="../"><input type="Submit" value="Back"></form>'
		
	

	
@app.route('/uploadimage', methods=['POST'])
def uploadimage():
    
    #out = """Successfully upload"""
	currentTime1 = datetime.datetime.now().time()
	currentTime = str(currentTime1)
	print  currentTime
	file_name = request.files['file_upload'].filename
	print file_name
	content = request.files['file_upload'].read()
	sizeOfFile = os.path.getsize(file_name)
	print sizeOfFile
	Comments = request.form['Comments']
	print Comments
	if len(Comments)<= comment_limit:
		out = "<h1>Successfully uploaded<h1>"
		encoded_string=base64.b64encode(content)
		postimage = {
                    #"username" : username,
                    "IMGBase64Data" : encoded_string,
                    "filename" : file_name,
                    "Time": currentTime,
                    #"description" : "First Image"
                    "description" : Comments
                    }
		post_id = collection.insert(postimage)
		return out
	
		
@app.route('/getmypictures', methods=['POST'])
def getmypictures():
    
            #query = collection.find({"username": username})
	returnString = ""
	for post in collection.find():
		IMGData = post['IMGBase64Data']
		print IMGData
		comments = post['description']
		#user_name = post['username']
		File_name = post['filename']
		Current_Time = post['Time']
		picdata = "data:image/jpeg;base64," + IMGData
		#print picdata
		appendString = '</br> <form id="/upload" action="../deletepicture" method="post"><input type="hidden" name= "filename" value="' + File_name + '"><input type="submit" value="Delete" id="submit_file"></form>'
		CommentString1 = '<form id="/upload" action="../updateComment" method="post"><input type="hidden" name= "filename" value="' + File_name + '"><input type="text" value=" " name="updatecomment"><input type="submit" value="UpdateComment" id="submit_file"></form>'
		returnString = '<img src={}>'.format(
                    picdata) + '<br>Comments:' + comments + '<br>File Name:' + File_name + '<br>Date Time:' + Current_Time +  appendString + returnString + CommentString1
        return returnString

@app.route('/removemypictures', methods=['POST'])
def removemypictures():
    
	query = collection.remove()
	out = "Deleted All Pictures"
	return out
        
if __name__ == "__main__":
    app.run(debug=True)