# Script to 
# 1. Get the list of all installed apps from Android device,
# 2. Get app information (like application name, package name, version name, version code),
# 3. Insert this information inside the portal.

from subprocess import call,check_output
import subprocess
import os, json
import pprint
from werkzeug import secure_filename
from datetime import datetime
import pickle

ALLOWED_EXTENSIONS =  set(['apk'])
# set(['csv','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

'''
Get the list of all the apps whos information is required
'''
def getRequirementAppList():
	#get user input
	reqAppList =[]
	print reqAppList
	return reqAppList


'''
Returns List for Info on each app.
Input: Path to extracted Apks folder
'''
def getAppInfo(path_to_extracted_apks):
	appInfo = []
	
	for apkfile in os.listdir(path_to_extracted_apks):
	    apkDetails =[]
	    if apkfile.endswith(".apk"):

	    	process1 = subprocess.Popen(["aapt", "d", "badging", path_to_extracted_apks + "/" + apkfile ], stdout=subprocess.PIPE)
	    	# Printing only the required badging information obtained from Process 1 
	    	# p1stdout = process1.stdout
	    	# process2 = subprocess.Popen(["grep", "package"], stdin=p1stdout, stdout=subprocess.PIPE)
	    	# process3 = subprocess.Popen(["grep", "application-label"], stdin=p1stdout, stdout=subprocess.PIPE)
	    	# print process1.communicate()[0]
	    	# process1.stdout.close()
	    	# print process1.communicate()[0]

	    	# Printing the stdOut tuple (process2.communicate()[0]) from the obtained results
	    	apkDetailsStr = process1.communicate()[0]
	    	# print "Json dumps output "
	    	# print json.dumps(apkDetailsStr)
	    	packageName = apkDetailsStr.split("package: name='")[1].split("' ")[0]
	    	versionCode = apkDetailsStr.split("versionCode='")[1].split("' ")[0]
	    	versionName = apkDetailsStr.split("versionName='")[1].split("' ")[0]
	    	platformBuildVersionName = apkDetailsStr.split("platformBuildVersionName='")[1].split("'")[0]
	    	applicationLabel = apkDetailsStr.split("application-label:'")[1].split("'")[0]

	    	apkDetails.append(packageName)
	    	apkDetails.append(versionCode)
	    	apkDetails.append(versionName)
	    	apkDetails.append(platformBuildVersionName)
	    	apkDetails.append(applicationLabel)

	    	appInfo.append([apkfile, apkDetails])
	    	# Write to file with timestamp
	    	# writeToFile(path_to_extracted_apks, apkInfo)

	## Pretty Printing the information    
	# print "Printing the App Info"
	# pprint.pprint(appInfo, depth=6)

	return appInfo

'''
Write apkInfo to a file with timestamp
'''
def writeToFile(path, apkInfo):
	filename = os.path.join(path , str(datetime.now().date()) + "_" + str(datetime.now().time()) + ".txt")
	# Method 1: Pickle method, scalable
	with open(filename, 'wb') as f:
		pickle.dump(apkInfo, f)

	# Method 2: Human Readable format, not scalable
	#Create a file Object with write permisions
	# fileObj = open(filename,"wb")
	# for item in apkInfo:
		# fileObj.write("%s\n" % item)

	msg = "Written to file!"
	return msg

'''
Read from all the files in the history folder
'''
def readAllFilesFolder(path):
	uploadHistory = []
	for historyfile in os.listdir(path):
		itemlist = []
		if historyfile.endswith(".txt"):
			print "Reading File " + historyfile + " ..."
			# Method 1: Pickle Method, better
			with open(os.path.join(path, historyfile), 'rb') as f:
				itemlist = pickle.load(f)
    		# Method 2: Human Readble Format but less scalable
    		# fileObj = open(filename,"rb")
			# itemlist = []
			# for line in fileObj:
				# itemlist.append(line)
			uploadHistory.append([historyfile, itemlist])
	
	# print "======== Upload History"
	# print uploadHistory
	return uploadHistory


'''
Check Allowed extensions
'''
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

'''
Upload Selected files to upload folder
'''
def uploadFiles(path_to_extracted_apks, fileList):
	print "====================="
	print "Uploading Files..."
	uploadCount = 0
	for apkfile in fileList:
		if apkfile and allowed_file(apkfile.filename):
			filename = secure_filename(apkfile.filename)
			apkfile.save(os.path.join(path_to_extracted_apks, filename))
			print "Uploading file " + apkfile.filename + " ..."
			uploadCount+=1
        else:
        	print apkfile.filename + " is not allowed to be uploaded."
	print str(uploadCount) + " files uploaded."
	return "Finished uploading. \n"


'''
Delete Uploaded Files
'''
def deleteUploadedFiles(path_to_extracted_apks):
	print "===================="
	print "Preparing to delete files from uploaded folder..."
	deleteCount = 0
	for apkfile in os.listdir(path_to_extracted_apks):
		print "Deleting file: " + apkfile
		deleteCount+=1
		#Method 1 :
		# subprocess.call(["rm", "-rf", path_to_extracted_apks + "/*"])

		'''
		Method 2 : Advantage over calling an external shell script is that it can be executed independently
		from external shells and system dependent external programs.
		'''
		file_path = os.path.join(path_to_extracted_apks, apkfile)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			#elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception, e:
			print e
	print str(deleteCount) + " files deleted."
	return "Finished deleting the APK files!"

if __name__ == "__main__":
	import sys
	test_apkInfo = getAppInfo("/Users/snehakulkarni/Documents/MSSE/MyProjectsAndLearning/PythonPrograms/Android/UploadExtractedApks")
	# print test_apkInfo
	writeToFile("/Users/snehakulkarni/Documents/MSSE/MyProjectsAndLearning/PythonPrograms/Android/UploadHistory/", test_apkInfo)
	readAllFilesFolder("/Users/snehakulkarni/Documents/MSSE/MyProjectsAndLearning/PythonPrograms/Android/UploadHistory")
	# deleteUploadedFiles(str(sys.argv[1]))
	# deleteUploadedFiles("/Users/snehakulkarni/Documents/MSSE/MyProjectsAndLearning/PythonPrograms/Android/UploadExtractedApks")
