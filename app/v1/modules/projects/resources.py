from flask_restplus import Resource, Namespace
from app.v1.extensions.auth.jwt_auth import auth
from app.v1.extensions.auth import role_required
from flask import request
from app import db
from app.v1.utils.projects_utils import save_projects,get_projects,projects_updating,delete_projects
from .serial import projects_reg,projects_update_list,projects_reg_model_list,projects_delete,update_projects_model

projects_ns=Namespace('projects')
parser=projects_ns.parser()
parser.add_argument('Authorization',
                    type=str,
                    required=False,
                    location='headers',
                    help='Bearer Access Token')

@projects_ns.route('/projects_create')
class projects_create(Resource):
    @projects_ns.expect(projects_reg,validate=True)
    def post(self):
        data=request.json
        print(data)
        return save_projects(data=data)
@projects_ns.route('/projects_list/<created_by>/')
class projects_listing(Resource):
    @projects_ns.marshal_list_with(projects_reg_model_list,envelope='data')     
    def get(self,created_by):
        return  get_projects(created_by)
@projects_ns.route('/projects_update')
class projects_update(Resource):
    @projects_ns.expect(projects_update_list,validate=True)
    def put(self):
        data=request.json
        return projects_updating(data)

@projects_ns.route('/delete_projects')
class project_delete(Resource):        
    @projects_ns.expect(projects_delete, validate=True)  
    def delete(self):
        data = request.json 
        return delete_projects(data=data)