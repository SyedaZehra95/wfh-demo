import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
from app import db
from bson import ObjectId


def get_encoded_faces():
    
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./profile_img/"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("./profile_img/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    
    #encode a face given the file name
    
    face = fr.load_image_file("./profile_img/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face():
    for filename in os.listdir('./visitors_img/'):
        print(filename)
   
        faces = get_encoded_faces()
        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())

        img = cv2.imread('./visitors_img/'+filename, 1)
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        #img = img[:,:,::-1]
        #img = cv2.VideoCapture(0)
    
        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                name=name.split('-')
                print(name)
                visitor_id=filename.split('-')
                id=visitor_id[1].split('.')
                db.db.Visitors.update_one({'_id':ObjectId(id[0])},{'$set':{'known':1,'name':name[1]}})

            face_names.append(name)
        os.remove('./visitors_img/'+filename)
        '''for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)'''


    # Display the resulting image
    '''while True:
        #ret,frame = img.read(1)cam

        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names '''





