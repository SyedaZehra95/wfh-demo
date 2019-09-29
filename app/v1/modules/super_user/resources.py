from flask_restplus import Resource, Namespace
from app.v1.extensions.auth.jwt_auth import auth
from app.v1.extensions.auth import role_required
from flask import request
from app import db
from app.v1.utils.super_user_utils import save_super_user,update_super_user,delete_super_user,new_registors,data_ActivateNewRegisters,data_RejectNewRegisters
from .serial import super_user_reg_model_list,update_super_user_update,update_model,super_user_delete,new_registors_data




super_user_ns = Namespace('super_user')
parser = super_user_ns.parser()
parser.add_argument('Authorization',
                    type=str,
                    required=False,
                    location='headers',
                    help='Bearer Access Token')

@super_user_ns.route('/super_user_create')
class super_create(Resource):     
    @super_user_ns.expect(super_user_reg_model_list, validate=True)    
    def post(self):
        data = request.json 
        print(data) 
        
        return save_super_user(data=data)

@super_user_ns.route('/super_user_delete')
class super_user_delete(Resource):        
    @super_user_ns.expect(super_user_delete, validate=True)  
    def delete(self):
        data = request.json 
         
        return delete_super_user(data=data)
    


@super_user_ns.route('/super_user_update')
class super_user_update(Resource):
    @super_user_ns.expect(update_super_user_update, validate=True)  
    def put(self):
        data = request.json 
        return update_super_user(data=data)


@super_user_ns.route('/NewRegistrationData')
class NewRegistrationData(Resource):
    @super_user_ns.marshal_list_with(new_registors_data,envelope='data')     
    def get(self):
        return new_registors()

@super_user_ns.route('/ActivateNewRegisters/<id>')
class ActivateNewRegisters(Resource):     
    def get(self,id):
        return  data_ActivateNewRegisters(id)


@super_user_ns.route('/RejectNewRegisters/<id>')
class RejectNewRegisters(Resource):     
    def get(self,id):
        return data_RejectNewRegisters(id)

