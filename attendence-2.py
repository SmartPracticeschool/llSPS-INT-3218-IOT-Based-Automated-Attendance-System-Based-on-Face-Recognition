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
#Provide your IBM Watson Device Credentials
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

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='qDP8ul5pmj-JeA-X59xTLeI9UNpncNoSRWRCimBcO-hZ')

#Provide CloudantDB credentials such as username,password and url

client=Cloudant("81126409-18c3-4170-8ec8-caa9c625a1f6-bluemix", "e117e4519d2e89da41b973c42037bfc171cafb6a61503cea672ca582dd23b389", url="https://81126409-18c3-4170-8ec8-caa9c625a1f6-bluemix:e117e4519d2e89da41b973c42037bfc171cafb6a61503cea672ca582dd23b389@81126409-18c3-4170-8ec8-caa9c625a1f6-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()

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
                classifier_ids='ATTENDANCE_931686589').get_result()
        print(json.dumps(classes, indent=2))



    for(ex,ey,ew,eh) in eyes:
        cv2.rectangle(frame, (ex,ey), (ex+ew,ey+eh), (127,0,255), 2)
        cv2.imshow('Face detection', frame)

    data={'Student1':'Prahas','Attendance percentage of prahas':'75','Student2':'Nikhila','Attendance percentage of nikhila':'75','Student3':'Vaishnavi','Attendance percentage of vaishnavi':'75','faculty1':'Greeshma','Attendance percentage of greeshma':'95' }
    def myOnPublishCallback():
        print(data)
    success=deviceCli.publishEvent("Weather","json",data,qos=0,on_publish=myOnPublishCallback)
    if not success:
        print("not connected")
    time.sleep(2)
    deviceCli.commandCallback=myCommandCallback


    #time.sleep(30)

    '''with open("./'{picname}'.jpg", 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file,
            threshold='0.6',
            classifier_ids='ATTENDANCE_931686589').get_result()
    print(json.dumps(classes, indent=2))'''


    #waitKey(1)- for every 1 millisecond new frame will be captured
    Key=cv2.waitKey(1)
    if Key==ord('q'):
        #release the camera
        video.release()
        #destroy all windows
        cv2.destroyAllWindows()
        break

deviceCli.disconnect()
