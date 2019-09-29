import datetime
import uuid
from flask import url_for,jsonify
from app import db
from datetime import datetime
from app.v1.helper.json_encoder import JSONEncoder
from bson import ObjectId
from app.v1.errors import CustomFlaskErr as notice
import string

def save_projects(data):
    projects_id = db.db.Projects.insert({
        "name":data['name'],
        "description":data['description'],
        "deadline":data['deadline'],
        "team":data['team'],
        "created_by":data['created_by'],
        "deleted":0,
        "created_at":datetime.now(),
        "updated_at":datetime.now(),      
        
    })
    return {"_id":JSONEncoder().encode(projects_id)}

    #return {"id":str(applications_id)}

def get_projects(created_by):
    print("get project",created_by)
    project=[]
    for pro in db.db.Projects.find({'created_by':created_by},{"name":1,"description":1,"deadline":1,"team":1}):
      project.append(pro)
      print(project)   
    return project
      
        

def projects_updating(data):
    print(data['_id'])
    print(data['update'])
    update_pro=db.db.Projects.update_one({'_id':ObjectId(data['_id'])},{'$set':data['update']})
    print(update_pro)
    if update_pro:
        return 1
    else:
        return 0

def delete_projects(data):
  print(data['_id'])
  project_delete=db.db.Projects.update_one({'_id':ObjectId(data['_id'])},{'$set':{'deleted':1}})
  print(project_delete)
  if project_delete:
    return 1
  else:
    return 0