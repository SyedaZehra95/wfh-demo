from flask_restplus import Resource, Namespace
from app.v1.extensions.auth.jwt_auth import auth
from app.v1.extensions.auth import role_required
from flask import request,Response
from app import db
from app.v1.utils.registration_utils import save_registration,login_registration,data_registration
from .serial import registration_reg_model,registration_login_model,registration_base_fram_model
from .serial import registration_base_fram_model
import work_registration as wr
import work_login as wl
import work_track as wt
registration_ns = Namespace('registration')
parser = registration_ns.parser()
parser.add_argument('Authorization',
                    type=str,
                    required=False,
                    location='headers',
                    help='Bearer Access Token')

@registration_ns.route('/register')
class registration_register(Resource):     
    @registration_ns.expect(registration_reg_model, validate=True)    
    def post(self):
       
        data = request.json 
        return save_registration(data=data)

@registration_ns.route('/login')
class registration_register(Resource):     
    @registration_ns.expect(registration_login_model, validate=True)    
    def post(self):
        data = request.json 
        return login_registration(data=data)

@registration_ns.route('/register_capture/<name>')
class registration_register(Resource):     
    def get(self,name):
        return  Response(wr.collect_faces(name), mimetype="multipart/x-mixed-replace; boundary=frame")

@registration_ns.route('/login_capture/<name>')
class registration_register(Resource):     
    def get(self,name):
        return 1 #wl.VerifyFace(name)

        

@registration_ns.route('/registration_track/<name>/<_id>/<stream>')
class registration_register(Resource):     
    def get(self,name,_id,stream):
        return  1#wt.RunExecutionPart(name,_id,stream)
            


@registration_ns.route('/track_stream/<name>/<_id>/<stream>')
class registration_register(Resource):     
    def get(self,name,_id,stream):
            return  1#Response(wt.RunExecutionPart(name,_id,stream), mimetype="multipart/x-mixed-replace; boundary=frame")

@registration_ns.route('/data/<_id>')
class registration_register(Resource):     
    def get(self,_id):
        return  data_registration(_id)



@registration_ns.route('/registration_base64_fram')
class registration_base64_fram(Resource):     
    @registration_ns.expect(registration_base_fram_model, validate=True)    
    def post(self):
        data = request.json 
        print('api')
        return data_fram_stream(data=data)









    
  
