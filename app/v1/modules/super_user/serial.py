

from app.v1 import v1_api

from flask_restplus import fields,Namespace

super_user_reg_model_list = v1_api.model('super_user_Reg', {
    
        'position': fields.String(required=True, description='position_name'),
        'role': fields.String(required=True, description='role_name'),
        #'deleted': fields.Integer(required=True, description='deleted')
      
})
update_model=v1_api.model('update_model',{
        'deleted': fields.Integer(required=True, description='deleted')
      
})
update_super_model=v1_api.model('update_super_model',{
        'position': fields.String(required=True, description='position_name'),
        'role': fields.String(required=True, description='role_name'),
        
        
})
update_super_user_update = v1_api.model('super_user_Reg_update', {
        '_id': fields.String(required=True, description='super_id'),
        'update':fields.Nested(update_super_model)
        
      
})

super_user_delete = v1_api.model('super_user_Reg_delete', {
        '_id': fields.String(required=True, description='super_id'),
})

new_registors_data = v1_api.model('new_registors_data',{

        'email': fields.String(required=True, description='email'),
        'FirstName':fields.String(required=True,description="FirstName"),
        'LirstName' : fields.String(required=True,description='LirstName'),
        'password' : fields.String(required=True,description='password'),
        'JobPositionId' : fields.Integer(required=True,description='jobpositionId'),
        'image' : fields.String(required=True,description='image')
})
