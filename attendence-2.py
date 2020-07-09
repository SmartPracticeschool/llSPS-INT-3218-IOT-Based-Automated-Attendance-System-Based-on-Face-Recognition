import cv2
import numpy as np
import datetime

import json
import time
import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

#Provide your IBM IoT Device Credentials
organization="5k0wq9"
deviceType="Bugga"
deviceId="654321"
authMethod="token"
authToken="87654321"

from watson_developer_cloud import VisualRecognitionV3

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import requests


face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_classifier=cv2.CascadeClassifier("haarcascade_eye.xml")

#VisualRecognition Service Credentials
visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='qDP8ul5pmj-JeA-X59xTLeI9UNpncNoSRWRCimBcO-hZ')


#Provide CloudantDB credentials such as username,password and url

client=Cloudant("2ff3b764-39d5-44fc-810f-24ca81359ee6-bluemix", "0acf9043d2850635230da1c615cb01f501659cf87cca8c0142243c1e20b9c33f", url="https://2ff3b764-39d5-44fc-810f-24ca81359ee6-bluemix:0acf9043d2850635230da1c615cb01f501659cf87cca8c0142243c1e20b9c33f@2ff3b764-39d5-44fc-810f-24ca81359ee6-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()

#Provide your database name

database_name = "atomated_attendence"

my_database = client.create_database(database_name)

if my_database.exists():
   print("'{database_name}' successfully created.")

# Initialize GPIO

def myCommandCallback(cmd):
    if cmd.data:
        print("Name1:Prahas","Attendance percentage of prahas:75",
             "\nName2:Nikhila","Attendance percentage of nikhila:75",
             "\nName3:Vaishnavi","Attendance percentage of vaishnavi:75",
             "\nName4:Greeshma","Attendance percentage of greeshma:75")


try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)#create client
        #.............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()#connect client to platform

#It will read the first frame/image of the video
video=cv2.VideoCapture(0)

while True:
    #capture the first frame
    check,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    #detect the faces from the video using detectMultiScale function
    faces=face_classifier.detectMultiScale(gray,1.3,5)
    eyes=eye_classifier.detectMultiScale(gray,1.3,5)
    print(faces)

    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (127,0,255), 2)
        cv2.imshow('Face detection', frame)
        picname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        cv2.imwrite(picname+".jpg",frame)
        with open(picname+'.jpg', "rb") as images_file:
            classes = visual_recognition.classify(
                images_file,
                threshold='0.6',
                classifier_ids='Attendence_834401690').get_result()
        if len(classes['images'][0]['classifiers'][0]['classes'])<1:
           print('Face not detected')
           continue
        img=classes['images'][0]['classifiers'][0]['classes'][0]['class']
        if img=='Others':
           continue
        else:
           print(img+' IS PRESENT')
        attendence=random.randint(75,80)
        #print(json.dumps(classes, indent=2))
        json_document={"Student_Name":img,"AttendencePercentage":attendence}
        new_document = my_database.create_document(json_document)
        # Check that the document exists in the database.
        if new_document.exists():
           print(f"Document successfully created.")
        data={'Student_Name':img,'AttendencePercentage':attendence}
        def myOnPublishCallback():
            print(data)
        success=deviceCli.publishEvent("Attendence","json",data,qos=0,on_publish=myOnPublishCallback)
        if not success:
            print("not connected")
        time.sleep(2)
        deviceCli.commandCallback=myCommandCallback

    for(ex,ey,ew,eh) in eyes:
        cv2.rectangle(frame, (ex,ey), (ex+ew,ey+eh), (127,0,255), 2)
        cv2.imshow('Face detection', frame)

    #waitKey(1)- for every 1 millisecond new frame will be captured
    Key=cv2.waitKey(1)
    if Key==ord('q'):
        #release the camera
        video.release()
        #destroy all windows
        cv2.destroyAllWindows()
        break

deviceCli.disconnect()
