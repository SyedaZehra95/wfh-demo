# -*- coding: utf-8 -*-
# @Author: chiranjeevi E
# @File Name: jwt_auth.py


from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

# JWT creation.
jwt = JWT('UbuQgGIdry*H&&I@', expires_in=6000)


# Refresh token creation.
refresh_jwt = JWT('Ag93ZQ3KcGg&KUhR', expires_in=17200)

# Email token creation
confirm_email_jwt = JWT('HuGIUMKXLoHi4Y2S', expires_in=17200)

# Auth object creation.
auth = HTTPTokenAuth('Bearer')

