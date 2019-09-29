import datetime
import uuid
from flask import url_for,jsonify
from app import db
from datetime import datetime
from app.v1.helper.json_encoder import JSONEncoder
from bson import ObjectId
from app.v1.errors import CustomFlaskErr as notice
import string
def save_applications(data):
    print(data)
    applications_id = db.db.Applications.insert({
        "app_name":data['app_name'],
        "created_by":data['created_by'],
        "url_app":data['url_app'],
        "img_app":data['img_app'],
        "role":data['role'],
        "enabled":data['enabled'],
        "created_at":datetime.now(),
        "updated_at":datetime.now(),      
        
    })
    return {"_id":JSONEncoder().encode(applications_id)}

    #return {"id":str(applications_id)}

def get_applications(created_by):
    role=[]
    print(created_by)
    for app in db.db.Applications.aggregate([{"$match":{u"enabled":1,u"created_by":created_by}},{"$lookup":{u"from":u"registration",u"localField":u"ObjectId(_id)",u"foreignField":u"ObjectId(created_by)",u"as":u"output1"}},{u"$unwind":u"$output1"},{"$project":{u"_id":1,u"role":u"$output1.role",u"app_name":1,u"url_app":1,u"img_app":1,u"enabled":1}}]):
        role.append(app)
    return role    

def create_applications(app_name,img_app,url_app,created_by,role):
    lst = []
    for data in db.db.Applications.find({'app_name':app_name,'img_app':img_app,'url_app':url_app,'created_by':created_by,'role':role}):
        print('for',data)
        lst.append(data)
    print(lst)
    return lst

def application_update_fields(data):
    res=[]
    print(created_by)
    for app in db.db.Applications.aggregate([{"$match":{"enabled":1}},{"$lookup":{u"from":u"registration",u"localField":u"ObjectId(_id)",u"foreignField":u"ObjectId(created_by)",u"as":u"output1"}},{"$project":{u"_id":1,u"role":u"$output1.role",u"app_name":1,u"url_app":1,u"img_app":1}}]):
        role.append(app)
        print(role)
    return role    

def application_update(data):
    print(data['_id'])
    print(data['update'])
    update_app=db.db.Applications.update_one({'_id':ObjectId(data['_id'])},{'$set':data['update']})
    print(update_app)
    if update_app:
        return 1
    else:
        return 0

    
