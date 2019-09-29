# -*- coding: utf-8 -*-
# @Author: chiranjeevi E
# @File Name: errors.py

from flask import make_response,jsonify
from app.v1 import v1_blueprint
from app.v1.extensions.auth.jwt_auth import auth

error_list = {
    0: "success",

    20001: "User does not exist",
    20002: "Account has been disabled",
    20003: "Invalid password",
    20004: "User does not exist",
    20005: "User not logged in",
    20006: "Invalid email address",
    20007: "Username and password cannot be empty",
    20008: "Account not activated",
    20009: "User activation failed, Invalid or the mailbox is incorrect, please contact the administrator.",

    # 用户成功：
    30000: "login successful",
    30001: "The account registration is successful, please click the activation link to activate the account.",
    30002: "The account has been activated successfully",

    # 参数错误：
    10001: "The parameter is empty",
    10002: "Invalid argument",
    10003: "Incorrect parameter type",
    10004: "Missing parameter",
}


PARAM_IS_INVALID = ({"message": "Invalid argument", "return_code": 10001 })
PARAM_IS_BLANK = ({"message": "The parameter is empty", "return_code": 10002 })
PARAM_TYPE_BIND_ERROR = ({"message": "Incorrect parameter type", "return_code": 10003 })
PARAM_NOT_COMPLETE = ({"message": "Missing parameter", "return_code": 10004 })

USER_NOT_LOGGED_IN = ({"message": "User not logged in", "return_code": 20001 })
USER_LOGIN_ERROR = ({"message": "The account does not exist or the password is incorrect.", "return_code": 20002,})
USER_ACCOUNT_FORBIDDEN = ({"message": "Account has been disabled", "return_code":20003})
USER_NOT_EXIST = ({"message": "User does not exist.", "return_code": 20004 })
USER_HAS_EXISTED = ({"message": "User already exists", "return_code": 20005})


SERVER_ERROR_500 = ({"message": "An error occured."}, 500)
NOT_FOUND_404 = ({"message": "Resource could not be found."}, 404)
NO_INPUT_400 = ({"message": "No input data provided."}, 400)
INVALID_INPUT_422 = ({"status":1,"message": "Invalid input."}, 422)

PASSWORD_INVALID_421 = ({"message": "Invalid password."}, 421)
ALREADY_EXIST = ({"status":1,"message": "Already exists."}, 409)

DOES_NOT_EXIST = ({"message": "Does not exists."}, 409)
NOT_ADMIN = ({"message": "Admin permission denied."}, 998)
HEADER_NOT_FOUND = ({"message": "Header does not exists."}, 999)

@auth.error_handler
def unauthorized():
    return make_response(jsonify(
        {   'status': 403,
            'message': 'Forbidden'
        }), 403)



class CustomFlaskErr(Exception):
    status_code = 400
    def __init__(self,status_code=None,return_code=None,action_status=None,playbook=None):
        super().__init__(self)
        self.return_code = return_code
        self.status_code = status_code
        self.action_status = action_status
        self.playbook = playbook
       
    def to_dict(self):
        rv = dict()
        if self.playbook != None:
            rv['data'] = self.playbook
        else:
            print (self.playbook)
        rv['action_status'] = self.action_status
        rv['message'] = error_list.get(self.return_code)
        rv['return_code'] = self.return_code
        rv['status_code'] = self.status_code
        print(rv)
        return rv

@v1_blueprint.app_errorhandler(CustomFlaskErr)
def handle_flask_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    print(response)

    return response

