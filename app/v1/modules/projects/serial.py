
from app.v1 import v1_api

from flask_restplus import fields,Namespace

projects_reg = v1_api.model('projects_Reg', {
    
        'name': fields.String(required=True, description='name'),
        'description': fields.String(required=True, description='description'),
        'deadline': fields.String(required=True, description='deadline'),
        'team': fields.List(fields.String, description='team'),
        'created_by': fields.String(required=True, description='created_by'),
        #'enabled': fields.Integer(required=True, description='enabled'),
        #'created_at': fields.String(required=True, description='created_at'),
        #'updated_at': fields.String(required=True, description='updated_at')

})

projects_reg_model_list = v1_api.model('projects_Reg_model_list', {
        'name': fields.String(required=True, description='name'),
        'description': fields.String(required=True, description='description'),
        'deadline': fields.String(required=True, description='deadline'),
        'team': fields.List(fields.String, description='team'),
})

update_projects_model=v1_api.model('update_model',{
        'name': fields.String(required=True, description='name'),
        'description': fields.String(required=True, description='description'),
        'deadline': fields.String(required=True, description='deadline'),
        'team': fields.List(fields.String, description='team'),        
})
projects_update_list = v1_api.model('projects_update_list', {
        '_id': fields.String(required=True, description='Application'),
        'update':fields.Nested(update_projects_model)     
})
projects_delete = v1_api.model('projects_Reg_delete', {
        '_id': fields.String(required=True, description='_id'),
})