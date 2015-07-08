from androidAppDetails import getAppInfo, uploadFiles, deleteUploadedFiles, writeToFile, readAllFilesFolder
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
from werkzeug import secure_filename


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'UploadExtractedApks/'
app.config['HISTORY'] = 'UploadHistory/'
ALLOWED_EXTENSIONS =  set(['apk'])
# # set(['csv','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#Setting global variable for appInfo
# NOTE: It will support at max 536,870,912 elements on a 32 bit system.
# Further the list size may significantly vary depending upon the RAM size of machine running this script.
# appInfo=[]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET','POST'])
def uploadApk():
    appInfo=[]
    # global appInfo
    msg = ""

    if request.method == 'GET':
        # if (apkPath in request.args & (not apkPath)):
            # PATH = apkPath
        print app.config['UPLOAD_FOLDER']
        appInfo = getAppInfo(app.config['UPLOAD_FOLDER'])

        # Read from the history file
        uploadHistory = readAllFilesFolder(app.config['HISTORY'])

        return render_template("index.html", apkInfo = appInfo, uploadHistory = uploadHistory)
    if request.method == 'POST':
        fileList = request.files.getlist('apkfile')

        #Uploading files
        msg = uploadFiles(app.config['UPLOAD_FOLDER'],fileList)

        # Refreshing appInfo Content
        appInfo = getAppInfo(app.config['UPLOAD_FOLDER'])

        #Storing upload history
        msg += writeToFile(app.config['HISTORY'], appInfo)

        # Deleting the contents of the UPLOAD_Folder
        msg += deleteUploadedFiles(app.config['UPLOAD_FOLDER'])

        # Read from the history file
        uploadHistory = readAllFilesFolder(app.config['HISTORY'])
        return render_template("index.html", apkInfo=appInfo, uploadHistory = uploadHistory, message=msg)

if __name__ == '__main__':
	app.run(host="0.0.0.0" , port = 5500, debug = True)
