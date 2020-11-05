import os
import argparse
import cv2
import numpy as np
import sys
import time
import requests
import json
import schedule
from datetime import datetime as time
import time as t
from datetime import date
import urllib
import math
from math import*
from threading import Thread
import importlib.util
import signal
import MySQLdb
import random
from time import sleep
import webbrowser, os, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
X=True

db = MySQLdb.connect(host="localhost", user="root", passwd="pass", db="comptage")
curs= db.cursor()

#Initialisation compteur cyclistes
counter = 0
#print(json.dumps({"cyclistes" : counter}))
lineCount = 80
curs.execute("UPDATE comptage SET cycliste=%i WHERE (id=1)" % (counter))
db.commit()

#Recuperation donnees JSON ATMO et envoi toutes les heures
url = 'https://api.openweathermap.org/data/2.5/weather?q=Lille,fr&appid=516e6363be8c13af250a48a49670e80e&units=metric'
res = requests.get(url)
data2 = res.json()

def requete(): #requete pour sur l'api d'ATMO
    v = time.today()
    today = date(v.year,v.month,v.day)# recuperation de la date du jour format Y-M-D
    # dictionnaire contenant les parametres de la requete
    payload = {"where" : "code_zone = '59350' AND date_ech >= TIMESTAMP '{}'".format(today), "outFields" : "date_ech,valeur,qualif,couleur", "outSR" : "4326",  "f" : "json"}
    param = urllib.parse.urlencode(payload, safe='='+',', quote_via=urllib.parse.quote) # encodage du dictionnaire des parametres
    r = requests.get('https://services8.arcgis.com/rxZzohbySMKHTNcy/arcgis/rest/services/ind_hdf_agglo/FeatureServer/0/query', params=param) # requete
    data1 = r.json()

    return releve(r) # appel de la fonction releve

schedule.every(30).minutes.do(requete)  

def releve(r): # recuperation des informations du releve
    data1 = r.json() # dictionnaire des données format json
    
    features = data1["features"][0]   #0 est l'indice du dernier releve
    attributes = features['attributes'] # toutes les informations du releve
    couleur = attributes["couleur"]
    quality = attributes["qualif"] # exemple de recuperation de la qualite de l'air du releve
    
    temp = data2['main']['temp']
    meteo = data2['weather'][0]['description']
    
    print("La temperature est de " + str(temp) + " degres celsius")
    print("Le ciel est de " + str(meteo))

    fichier(data1,r,couleur,quality,temp,meteo)   
    return couleur, quality, temp, meteo # renvoi de la donnee qui nous intéresse

def fichier(data1,r,couleur,quality,temp,meteo): # fonction permettant d'enregistrer les données recuperées dans un fichier json (optionel)
    file = open('/var/www/html/' + 'dataAPI2.js','w')
    file.write("data='" +r.text+"';\n"
               +"couleur='" +str(couleur)+"';\n"
               +"quality='" +str(quality)+"';\n"
               +"temp='" +str(round(temp))+"';\n"
               +"meteo='" +str(meteo)+"';\n")
    file.close()

def comptage(): # fonction permettant d'enregistrer le comptage de velo recuperé dans un fichier json (optionel)
    file = open('/var/www/html/' + 'comptage.json','w')
    file.write("data2=" + json.dumps({"cyclistes" : counter}))
    file.close()
schedule.every(5).seconds.do(comptage)

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/

class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(620,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True)
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.5)
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='1280x720')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = args.edgetpu

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Initialize video stream
videostream = VideoStream(resolution=(imW,imH),framerate=30).start()
requete()
#comptage()
#for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
while X==True:
    schedule.run_pending()

    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    # Grab frame from video stream
    frame1 = videostream.read()
    # Acquire frame and resize to expected shape [1xHxWx3]
    frame = frame1.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()
    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
    #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)
    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))

            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255,0), 2)
            cv2.line(frame,(lineCount,0),(lineCount,1080),(0,255,255),2)
        # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            #print(object_name)
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
            if object_name== 'person':
            	if xmin<=lineCount:
            		counter=counter+1
            		print(counter)
            		print("Felicitations vous etes le " + str(counter) +" eme  cyclistes")
            		curs.execute("UPDATE comptage SET cycliste=%i WHERE (id=1)" % (counter))
            		db.commit()
            		t.sleep(1)
            	else:
            		counter=counter
            else:
            	continue
    # Draw framerate in corner of frame
    cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)

    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)
    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc= 1/time1

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break
# Clean up
cv2.destroyAllWindows()
videostream.stop()
