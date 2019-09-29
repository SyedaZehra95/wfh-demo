import numpy as np 
import matplotlib.pyplot as plt 

import cv2 
import tensorflow as tf 

import tensorflow.keras as keras 

import dlib 
import face_recognition 
from imutils import face_utils 

from tensorflow.keras.models import load_model 

import pickle 

from collections import OrderedDict 

def Output_FER(pred):
    
    if pred == 0:
        return "Angry"
    
    elif pred == 1 :
        return "Disgust"
    
    elif pred == 2 :
        return "Fear"
    
    elif pred == 3 :
        return "Happy"
    
    elif pred == 4 :
        return "Sad"
    
    elif pred == 5 :
        return "Surprise"
    
    else :
        return "Neutral"
    
def ProcessImage_FER( Img , resize = True , size = 64 , Normalize = True , blur = True): 
    
    if Normalize == True :
        Img = Img / 255.0
        
    if resize == True :
        Img = cv2.resize( Img , (size , size) )
        
    if blur == True :
        Img = cv2.GaussianBlur( Img , (5,5) , 0 ) 
        
    return Img 

params_fer = open("params.npy")

def Predict_FER(graph , session , model , gray , params):
    Img = ProcessImage_FER(gray)

    Img = Img.reshape(1,64,64,1)

    Img = (Img - params[0]) / params[1]

    with graph.as_default():
        with session.as_default():
            pred = model.predict(Img)

    index = np.argmax(pred)
    #confidence = pred[index]
    out = Output_FER(index)
    
    return out

# Loading FER model

graph = tf.Graph()
with graph.as_default():
    session = tf.compat.v1.Session()
    with session.as_default():
        model_fer = load_model('model_fer_complete.h5')
            
graph_fer = graph
session_fer = session

def no_of_occuring(lis):
    unique = list(set(lis))
    dic = {}
    
    for i in unique :
        dic[i] = 0
    
    for i in lis :
        dic[i] = dic[i] + 1 
        
    return max(dic.values()) < 15

def get_index(given_name , search_names):
    for i,j in enumerate(search_names):
        if given_name == j :
            return i
        if i == len(search_names) - 1 :
            return "NotFound"

detector = dlib.get_frontal_face_detector()

def VerifyFace(a):
	pickle_in = open("names_to_encodings.pickle","rb")
	dic = pickle.load(pickle_in)
	print(a)
	Cam = cv2.VideoCapture(0)

	process_frame = True
	print(process_frame)

	names = list(dic['names'])
	print(names)
	encodings_all = list(dic['encodings'])

	index = get_index(a , names)
	encodings = encodings_all[index]

	count = 0 

	Welcome = False
	Send_me_in = False 

	expressions = []

	while True :
	    
	    ret , frame = Cam.read()
	    print(index)
	    
	    gray_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
	    
	    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	    small_frame = small_frame[:, :, ::-1]
	    
	    rects = detector(gray_frame, 0)
	    
	    if len(rects) > 1 or len(rects) == 0:
                
	        continue
	    
	    else :
	        for rect in rects :
	            (x , y , w , h) = face_utils.rect_to_bb(rect)
	            gray = gray_frame[y : y + h , x : x + w]
	            output_fer = Predict_FER(graph_fer , session_fer , model_fer , gray , params_fer)
	            #dictionary[output_fer].append(confidence_fer)
	            expressions.append(output_fer)
	    
	    if process_frame :
	        face_locations = face_recognition.face_locations(small_frame)
	        print('here')
	        face_encodings = face_recognition.face_encodings(small_frame , face_locations)
	        
	    if len(face_encodings) == 1 :
	        face_encoding = face_encodings[0]
	    else :
	        print(" More infront of Camera ")
	        break
	        
	    distances = []
	    
	    for encoding in encodings :
	        distance = np.linalg.norm(encoding - face_encoding)
	        distances.append(distance)
	        
	    if 0.1 < min(distances) < 0.4 or 0.3 < max(distances) < 0.6 :
	        Welcome = True
	        if Welcome :
	            Send_me_in = True
	            if len(set(expressions)) > 1 :
	                break
	        
	    count = count + 1
	    
	    if count == 15 :
	        break
	        
	if Send_me_in and (no_of_occuring(expressions) or len(set(expressions)) > 1) :
		print(" Welcome " + a)
		return 1
		#return face_locations

	else :
	    print(" Person Not Found ")
	    return 0
	    #return face_locations

	#Cam.release()
	#cv2.destroyAllWindows()

	

#name = input(" Enter Name ? ")
#face_locations = VerifyFace(name)
