from flask_restplus import Resource, Namespace
from app.v1.extensions.auth.jwt_auth import auth
from app.v1.extensions.auth import role_required
from flask import request
from app import db
from app.v1.utils.applications_utils import save_applications,get_applications,create_applications,application_update_fields,application_update
from .serial import applications_reg_model_list,applications_reg,application_updates_fields,applications_reg_list,application_updates,update_applications_model


applications_ns = Namespace('applications')
parser = applications_ns.parser()
parser.add_argument('Authorization',
                    type=str,
                    required=False,
                    location='headers',
                    help='Bearer Access Token')

@applications_ns.route('/applications_create')
class applications_create(Resource):     
    @applications_ns.expect(applications_reg, validate=True)    
    def post(self):
        data = request.json 
        print(data) 
        return save_applications(data=data)

@applications_ns.route('/applications_list/<created_by>/')
class applications_listing(Resource):
    @applications_ns.marshal_list_with(applications_reg_model_list,envelope='data')     
    def get(self,created_by):
        print('resouressssssssssssssssssssss',created_by)
        return  get_applications(created_by)

@applications_ns.route('/create/<app_name>/<img_app>/<url_app>/<created_by>/<role>/')
class create(Resource):
    @applications_ns.marshal_list_with(applications_reg_list,envelope='data')     
    def get(self,app_name,img_app,url_app,created_by,role):
        print('resouress',app_name,img_app,url_app,created_by,role)
        return  create_applications(app_name,img_app,url_app,created_by,role)

@applications_ns.route('/update_fields')
class applications_update_fields(Resource):
 @applications_ns.expect(application_updates_fields,validate=True)
 def put(self):
    data=request.json
    return application_update_fields(data)
        #print(created_by)
    #return  get_applications(created_by)

@applications_ns.route('/applications_update')
class applications_update(Resource):
    @applications_ns.expect(application_updates,validate=True)
    def put(self):
        data=request.json
        return application_update(data)
