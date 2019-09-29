from app.v1 import v1_api

from flask_restplus import fields,Namespace


registration_reg_model = v1_api.model('registration_Reg', {
        'email': fields.String(required=True, description='email'),
        'FirstName':fields.String(required=True,description="FirstName"),
        'LastName' : fields.String(required=True,description='LirstName'),
        'password' : fields.String(required=True,description='password'),
        'JobPositionId' : fields.String(required=True,description='jobpositionId'),
        'image' : fields.String(required=True,description='image')
 
      
})

registration_login_model = v1_api.model('registration_login', {
        'email': fields.String(required=True, description='zone name'),
        'password' : fields.String(required=True,description='delete_data')
 
      
})


registration_base_fram_model = v1_api.model('registration_base_fram_model',{
 #'_id': fields.String(required=True, description='Application'),
 'base64':fields.String(required = True,description='base64')
})

