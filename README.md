# Android-Apk-Info
This script reads the information about an android apps extracted from mobile.

## What this script does?
1. Checks for the extracted apks for format.
2. Can upload one or more files to the server.
3. Runs "aapt d badging (apk_path)" command to obtain APK File Name, Application Name, Package Name, Build Version Name, Version Code, and Platform Build Version Name information.
4. Delete the Apk files uploaded from the server.
5. Store the results in a consolidates history seggregated by date and time.

## Requirements and Assumptions
Requirements: Adb, flask and python installed on the machine.
Assumptions: You have the extracted Apk files in a folder to upload.

## How to Run this script
Step 1. Install and Check all dependencies.
Step 2. Run the apkInfo.py script in the terminal using command: python apkInfo.py
Step 3. Open the browser go to "http://localhost:5500".
Step 4. Upload all the apk files and click submit.
Step 5. Optionally, you can check all the history from the history tab.
