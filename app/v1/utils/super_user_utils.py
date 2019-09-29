

import datetime
import uuid
from flask import url_for,jsonify
from app import db
from datetime import datetime
from app.v1.helper.json_encoder import JSONEncoder
from bson import ObjectId
from app.v1.errors import CustomFlaskErr as notice
import string
def save_super_user(data):
    print(data)
    super_user = db.db.Super_user.insert({
        "position":data['position'],
        "role":data['role'],
        "deleted":0,
        "created_at":datetime.now(),
        "updated_at":datetime.now(),      
        
    })
    
    return {"id":str(super_user)}

def update_super_user(data):
    print(data['_id'])
    print(data['update'])
    update_super=db.db.Super_user.update_one({'_id':ObjectId(data['_id'])},{'$set':data['update']})
    print(update_super)
    if update_super:
        return 1
    else:
        return 0

def delete_super_user(data):
  super_delete=db.db.Super_user.update_one({'_id':ObjectId(data['_id'])},{'$set':{"deleted":1}})
  print(super_delete)
  if super_delete:
    return 1
  else:
    return 0



def new_registors():
  lst = []
  #for data in db.db.registration.find({'isActive':1},{'deleted':0}):
  for data in db.db.registration.find({'isActive':0,'deleted':0},{'email':1,'FirstName':1,'LirstName':1,'password':1,'JobPositionId':1,'image':1}):
    print(data)
    lst.append(data)
  return lst


def data_ActivateNewRegisters(id):
  print(id)
  #print(data['_id'])
  super_active=db.db.registration.update_one({'_id':ObjectId(id),'isActive':0,'deleted':0},{'$set':{"isActive":1}})
  print(super_active)
  if super_active:
    return 1
  else:
    return 0

def data_RejectNewRegisters(id):
  print(id)
  #print(data['_id'])
  super_reject=db.db.registration.update_one({'_id':ObjectId(id),'deleted':0},{'$set':{'deleted':1}})
  print(super_reject)
  if super_reject:
    return 1
  else:
    return 0
