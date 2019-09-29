from app.v1 import v1_api

from flask_restplus import fields,Namespace

applications_reg = v1_api.model('applications_Reg', {
    
        'app_name': fields.String(required=True, description='position_name'),
        'created_by': fields.String(required=True, description='role_name'),
        'url_app': fields.String(required=True, description='url_app'),
        'img_app': fields.String(required=True, description='img_app'),
        'role': fields.List(fields.String, description='role'),
        'enabled': fields.Integer(required=True, description='enabled'),
        #'created_at': fields.String(required=True, description='created_at'),
        #'updated_at': fields.String(required=True, description='updated_at')

})


applications_reg_model_list = v1_api.model('applications_reg_model_list', {
        #'id': fields.String(required=True, description='id'),
        'app_name': fields.String(required=True, description='position_name'),
        'url_app': fields.String(required=True, description='url_app'),
        'img_app': fields.String(required=True, description='img_app'),
        'enabled': fields.Integer(required=True, description='enabled'),
        #'created_at' : fields.String(required=True,description='created date'),
})


applications_reg_list = v1_api.model('applications_reg_list', {
    
        'app_name': fields.String(required=True, description='position_name'),
        'created_by': fields.String(required=True, description='role_name'),
        'url_app': fields.String(required=True, description='url_app'),
        'img_app': fields.String(required=True, description='img_app'),
        'role': fields.List(fields.String(description='role')),
        'enabled': fields.Integer(required=True, description='enabled'),
        'created_at': fields.String(required=True, description='created_at'),
        'updated_at': fields.String(required=True, description='updated_at')

})


update_model=v1_api.model('update_model',{
        'app_name': fields.String(required=True, description='position_name'),
        'url_app': fields.String(required=True, description='url_app'),
        'img_app': fields.String(required=True, description='img_app'),
        'role': fields.List(fields.String(description='role')),
 
 
})
application_updates_fields = v1_api.model('application_updates_fields', {
 '_id': fields.String(required=True, description='Application'),
 'update':fields.Nested(update_model)
})

registration_base_fram_model = v1_api.model('registration_base_fram_model',{
 #'_id': fields.String(required=True, description='Application'),
 'base64':fields.String(required=True, description='base64'),
        #'enabled': fields.Integer(required=True, description='enabled'),
        #'created_at' : fields.String(required=True,description='created date'),
})

update_applications_model=v1_api.model('update_applications_model',{
        'enabled': fields.Integer(required=True, description='enabled'),
        
        
})
application_updates = v1_api.model('application_updates', {
        '_id': fields.String(required=True, description='Application'),
        'update':fields.Nested(update_applications_model)
        
      
})