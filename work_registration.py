import numpy as np
import matplotlib.pyplot as plt 

import cv2 

import dlib 
import face_recognition 

from imutils import face_utils

import pickle

# Loading Saved pickle files if exist 
from pathlib import Path

'''
check_dic = Path("names_to_encodings.pickle")

# Check if path exists or else make the file and keep it empty
if check_dic.is_file():
    pickle_name = open("names_to_encodings.pickle","rb")
    names_to_encodings = pickle.load(pickle_name)
else :
    names_to_encodings = {'names' : [] , 'encodings' : []}
'''

# Saving the Face Images 
# Enrolling a Face 

# When you get the username , pass the username as an argument for this function 

def collect_faces(name):
	check_dic = Path("names_to_encodings.pickle")

	if check_dic.is_file():
		pickle_name = open("names_to_encodings.pickle","rb")
		names_to_encodings = pickle.load(pickle_name)
	else :
		names_to_encodings = {'names' : [] , 'encodings' : []}
		
	Cam = cv2.VideoCapture(0)

	collect_encodings = []

	while True :
	    ret , Frame = Cam.read()
	    
	    if not ret :
	        break
	        
	    Frame_rgb = cv2.cvtColor(Frame , cv2.COLOR_BGR2RGB)
	    Frame_gray = cv2.cvtColor(Frame , cv2.COLOR_BGR2GRAY)
	    
	    boxes = face_recognition.face_locations(Frame_rgb , model='hog')
	    
	    encodings=[]
	    if len(boxes) == 1 :
	        encodings = face_recognition.face_encodings(Frame_rgb , boxes)[0]
	        boxes = boxes[0]
	        top , right , bottom , left = boxes
	    
	    if len(encodings) == 128 :
	        collect_encodings.append(encodings)
	        
	    else :
	        break
	        
	    cv2.rectangle(Frame , (left , top), (right, bottom),(0, 255, 0), 2)
	    _,frame=cv2.imencode(".jpg",Frame)
	    frame = frame.tobytes()
	    yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n"+frame+b"\r\n\r\n")
		
	    if len(collect_encodings) == 30 :
	        break
	        
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	if len(collect_encodings) > 0:
	    names_to_encodings['names'].append(name)
	    names_to_encodings['encodings'].append(collect_encodings)

	pickle_out = open("names_to_encodings.pickle","wb")
	pickle.dump(names_to_encodings, pickle_out)
	pickle_out.close()
	    
	Cam.release()
	cv2.destroyAllWindows()

 


#name = input()
#collect_faces(name)
