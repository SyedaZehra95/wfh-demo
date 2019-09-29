import numpy as np 

import cv2 
import tensorflow as tf 

import tensorflow.keras as keras 

import dlib 
import face_recognition 
from imutils import face_utils 

from tensorflow.keras.models import load_model 

import pickle
from bson import ObjectId
from app import db
from collections import OrderedDict 

def no_of_occuring(lis):
    unique = list(set(lis))
    dic = {}
    
    for i in unique :
        dic[i] = 0
    
    for i in lis :
        dic[i] = dic[i] + 1 
        
    return max(dic.values()) < 15

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
predictor_2 = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Loading the Face Expression Recognition Model 

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

params_fer = open("params_wrk.npy")

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
        model_fer = load_model('model_wrk_complete.h5')
            
graph_fer = graph
session_fer = session

pickle_in = open("names_to_encodings.pickle","rb")
dic = pickle.load(pickle_in)

def get_index(given_name , search_names):
    for i,j in enumerate(search_names):
        if given_name == j :
            return i
        if i == len(search_names) - 1 :
            return "NotFound"

#top , right , bottom , left = face_locations[0]

#best_centroid = np.array([left + (right - left)/2 , top + (bottom - top)/2])

def CheckMultiple(img):
    boxes = face_recognition.face_locations(img)
    return len(boxes) != 1

def recognize_face(img , copy_frame_gray , encodings):
    rects = detector(copy_frame_gray, 0)
    
    if len(rects) > 1 :
        #print(" I went here ")
        return False , None
    
    img = cv2.resize(img , (0, 0), fx=0.25, fy=0.25)
    
    boxes = face_recognition.face_locations(img)
    
    face_encodings = face_recognition.face_encodings(img, boxes)
    
    if len(boxes) != 1 :
        return False , None 
    
    top , right , bottom , left = boxes[0]
    
    centroid = np.array([left + (right - left)/2 , top + (bottom - top)/2])

    if len(face_encodings) == 1 :
        face_encoding = face_encodings[0]
    else :
        return False , None
    
    distances = []
    
    for encoding in encodings :
        distance = np.linalg.norm(encoding - face_encoding)
        distances.append(distance)
        
    #print(min(distances) , max(distances))
        
    return (0.2 < min(distances) < 0.5 or 0.3 < max(distances) < 0.7) , centroid

def distance(pt1 , pt2):
    return np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)

def GetRatio(shape):
    Right = distance(shape[3],shape[30])
    Left = distance(shape[30],shape[13])
    
    return Right/Left

def shape_np_array(shape):
    
    co_ordinates = np.zeros((68,2) , dtype = "int")
    
    for i in range(0,68):
        co_ordinates[i] = (shape.part(i).x , shape.part(i).y)
        
    return co_ordinates

from scipy.spatial import distance as dist

class CentroidTracker():
    def __init__(self, maxDisappeared=50):
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()

        self.maxDisappeared = maxDisappeared
        
    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        if len(rects) == 0:
            for objectID in self.disappeared.keys():
                self.disappeared[objectID] += 1

                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)

            return self.objects

        inputCentroids = np.zeros((len(rects), 2), dtype="int")

        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])

        else:
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())

            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            usedRows = set()
            usedCols = set()

            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue

                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0

                usedRows.add(row)
                usedCols.add(col)

            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1

                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)

            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])

        return self.objects

from scipy.stats import mode 
import pandas as pd

import numpy as np

def distance(a , b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_closest_index(a , b):
    min_dist = np.Inf
    count = 0
    for i in b :
        d = distance(a , i)
        if d < min_dist :
            min_dist = d 
            index = count
        count = count + 1
    return index

def check_recognition_log(lis):
    values = lis[-3:]
    
    if len(set(values)) == 1 :
        if list(set(values))[0] == False :
            return False
        else :
            return True
    else :
        return True 

Tracker = CentroidTracker(maxDisappeared = 40) # Object for facial tracking

# Keep Appending the Expressions , 
# Pie charks , Bar Graphs are must 

import time 

# Takes in the parameter the UserName 
def RunExecutionPart(UserName,_id,stream):
	pickle_in = open("names_to_encodings.pickle","rb")
	dic = pickle.load(pickle_in)
	names = list(dic['names'])
	print(names)
	tic=time.time()
	encodings_all = list(dic['encodings'])

	index = get_index(UserName , names)
	encodings = encodings_all[index]

	Cam = cv2.VideoCapture(0)

	tic = time.time()
	# Warning Counters
	multiple_warning_counter = 0
	no_persons_counter = 0

	# Total runtime Counter 
	total_counter = 0

	# Attention Counters 
	attention_counter = 0
	no_attention_counter = 0

	# Looks Counters 
	right_counter = 0
	left_counter = 0
	straight_counter = 0

	previous_finding = ""
	current_finding = ""

	recognition_log = []

	while True :
	    
	    total_counter += 1 
	    
	    ret , frame = Cam.read()
	    
	    output_fer = ""
	    
	    # If there's no frame coming , then break the execution 
	    if not ret:
	        toc = time.time()
	        #print(" I went to frame not read ")
	        break
	        
	    copy_frame_gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
	    copy_frame_rgb = frame[:, :, ::-1]
	    
	    # We need to check face for every 5 minutes 
	    toc = time.time()
	    
	    if ((int(toc - tic) + 1)%60) == 0 and (int(toc - tic) + 1)/60 % np.random.randint(1,6) == 0 :
	        #print(" I've done the face recognition ")
	        boolean , best_centroid_current = recognize_face(copy_frame_rgb , copy_frame_gray , encodings)
	        #print(boolean)
	        recognition_log.append(boolean)
	            
	        if best_centroid_current is not None :
	            best_centroid = best_centroid_current 
	        else :
	            best_centroid = best_centroid
	            
	        if len(recognition_log) > 3 :
	            continue_or_not = check_recognition_log(recognition_log)
	            if not continue_or_not :
	                break
	    
	    # Get the rectangles axis to be drawn on frame 
	    rects = detector(copy_frame_gray, 0)
	    
	    rectangles = []
	    rectangles_2 = []
	    
	    # This will be adding Red Boxes around the Faces 
	    
	    if len(rects) > 0 :
	        for rect in rects :
	            ( x , y , w , h ) = face_utils.rect_to_bb(rect)
	            rectangles.append([x , y , w + x , y + h])
	            rectangles_2.append([x , y , w , h])
	            cv2.rectangle(frame , (x, y), (x+w, y+h),(0, 0, 255), 1)
	            
	        best_centroid = np.array([int(x + w/2) , int(y + h/2)])
	        # Update the Tracker object if any faces found 
	        Objects = Tracker.update(rectangles)
	        
	    # If No faces found , set the Objects to a empty dictionary
	    else :
	        Objects = {}
	    
	    # If more than 1 person in front of camera (Continous), Alert !!!!!!
	    if len(rects) > 1:
	        multiple_warning_counter += 1
	        if multiple_warning_counter % 10 == 0 :
	            cv2.putText(frame," Multi Person Alert : " + str(multiple_warning_counter) , (100, 100),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
	            
	    else :
	        multiple_warning_counter = 0
	        
	        
	    # If No person infront of camera (Continous) , Alert !!!!!!!!
	    if len(rects) == 0:
	        no_persons_counter += 1 
	        if no_persons_counter % 10 == 0 :
	            cv2.putText(frame ," No person Alert : " + str(no_persons_counter) , (400 , 400) , cv2.FONT_HERSHEY_SIMPLEX , 1 , (255 , 255 , 0) , 2)
	    else :
	        no_persons_counter = 0
	        
	    # if Countdown Completed , break and take a not of timestamp [More than 1 person]
	    if multiple_warning_counter == 150 :
	        toc = time.time()
	        #print(" I went to Multiple person Alert ")
	        break
	        
	    # if Countdown Completed , break and take a not of timestamp [No persons]
	    if no_persons_counter == 600 :
	        toc = time.time()
	        #print(" I went to No person Alert ")
	        break
	        
	    # Important Boolean , for the first frame
	    first = True 
	    
	    # Loops on the faces
	    for rect in rects :
	        #print(" I got faces ")
	        (x , y , w , h) = face_utils.rect_to_bb(rect)
	        gray = copy_frame_gray[y : y+h , x : x+w]
	        rgb = copy_frame_rgb[y : y+h , x : x+w]
	        
	        current_centroid = np.array([int(x + w/2) , int(y + h/2)])
	        #print(current_centroid)
	        # If only 1 person , get the closest centroid to current centroid 
	        if len(Objects) == 1 :
	            #print(list(Objects.values()))
	            current_index = get_closest_index(current_centroid , np.array(list(Objects.values())))
	            text = "ID {}".format(list(Objects.keys())[current_index])
	            finding = text
	        # If 0 or more than 1 , 
	        elif len(Objects) > 1 :
	            current_index = get_closest_index(best_centroid , list(Objects.values()))
	            best_centroid = np.array(list(Objects.values())[current_index])
	            text = "ID {}".format(list(Objects.keys())[current_index])
	            finding = text
	            
	        
	        # If its the first frame , get the closest to the centroid where the face was recognized 
	        if first :
	            current_index = get_closest_index(best_centroid , list(Objects.values()))
	            best_centroid = np.array(list(Objects.values())[current_index])
	            text = "ID {}".format(list(Objects.keys())[current_index])
	            finding = text
	            first = False 
	        
	        if (gray.shape[0] != 0 and gray.shape[1] != 0) and (rgb.shape[0] != 0 and rgb.shape[1] != 0) :
	            output_fer = Predict_FER(graph_fer , session_fer , model_fer , gray , params_fer)
	            
	        shape = predictor(copy_frame_gray , rect)
	        shape = face_utils.shape_to_np(shape)

	        shape_2 = predictor_2(copy_frame_gray , rect)
	        shape_2 = shape_np_array(shape_2)

	        Tot_R = GetRatio(shape_2)

	        if Tot_R > 2 :
	            att_2 = " Looking Left "
	            left_counter += 1 
	        elif Tot_R < 0.5 :
	            att_2 = " Looking Right "
	            right_counter += 1 
	        else :
	            att_2 = ""
	            straight_counter += 1 

	        ratio = distance(shape[0],shape[2]) / distance((shape[0] + shape[2])/2,shape[4])

	        if ratio < 1.62:
	            att = "not paying attention"
	            no_attention_counter += 1 

	        else :
	            att = "paying attention"
	            attention_counter += 1
	        
	        
	        if finding == text:
	            cv2.rectangle(frame, (x, y), (x+w, y+h),(0, 255, 0), 1)
	            z = y - 15 if y - 15 > 15 else y + 15
	            cv2.putText(frame, output_fer + " , " + att + " ," + att_2, (x - 10, y - 30), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 1)
	            break
                    
	 
	    #cv2.imshow("frame" , frame)
	    _,frame=cv2.imencode(".jpg",frame)
	    frame = frame.tobytes()
	    yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n"+frame+b"\r\n\r\n")
	 
	
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
	        
	Cam.release()
	cv2.destroyAllWindows()
	toc=time.time()
	total_time=toc-tic
	attention_percent=float((attention_counter)/(attention_counter + no_attention_counter))*100
	left_percentage=float((left_counter)/(left_counter + right_counter + straight_counter))*100
	right_percentage=float((right_counter)/(left_counter + right_counter + straight_counter))*100
	work=db.db.Work_tracker.insert({
            'user_id':ObjectId(_id),
            'tot_time':total_time,
            'attention_percentage':attention_percent,
            'left_percentage':left_percentage,
            'right_percentage':right_percentage
            })
	return [attention_counter , no_attention_counter , left_counter , right_counter , straight_counter]

# Dont forget to send username 
# 
'''tic = time.time()
Stats = RunExecutionPart("zehra") # Just example purpose , update the name according to need 
toc = time.time()

attention_counter , no_attention_counter , left_counter , right_counter , straight_counter = Stats 

# We need to store these stats some where to show the graphs 
print(" Total Time in Seconds : " , toc - tic)
print(" Attention Percentage : " , float((attention_counter)/(attention_counter + no_attention_counter)))
print(" Left Percentage : " , float((left_counter)/(left_counter + right_counter + straight_counter)))
print(" Right Percentage : " , float((right_counter)/(left_counter + right_counter + straight_counter)))'''
