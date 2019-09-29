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

def get_index(given_name , search_names):
    if given_name not in search_names :
        return "NotFound"
    
    for i,j in enumerate(search_names):
        if given_name == j :
            return i

def RunExecutionPart(username):
    pickle_in = open("names_to_encodings.pickle","rb")
    dic = pickle.load(pickle_in)
    
    names = list(dic['names'])
    encodings_all = list(dic['encodings'])
    
    index = get_index(username , names)
    
    if index == "NotFound":
        return (" UserName : " , username , " Not Found")
    
    else :
        dic['names'].pop(index)
        dic['encodings'].pop(index)
        
        print(" User with Name : " , username , " Deleted ")
        
    pickle_out = open("names_to_encodings.pickle","wb")
    pickle.dump(dic, pickle_out)
    pickle_out.close()


