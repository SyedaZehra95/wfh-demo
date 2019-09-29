
from flask import Blueprint
from flask_restplus import Api

v1_blueprint = Blueprint('v1_blueprint', __name__,
                        template_folder='templates')

# Bases Authorization
# authorizations = {
#     'apiKey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'Authorization'
#     }
# }

v1_api = Api(v1_blueprint,
            title='WORK_FROM_HOME_API',
            version='1.0',
            description='auth: CHIRANJEEVI E',
            default="auth", 
            default_label=''
            # authorizations=authorizations,
            # security='apiKey')
            )






from .modules.registration.resources import registration_ns
from .modules.super_user.resource import super_user_ns
from .modules.applications.resource import applications_ns
from .modules.projects.resources import projects_ns


v1_api.add_namespace(registration_ns)
v1_api.add_namespace(super_user_ns)
v1_api.add_namespace(applications_ns)
v1_api.add_namespace(projects_ns)


