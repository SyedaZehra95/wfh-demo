from datetime import datetime
import uuid
from flask import url_for,jsonify
from app import db
from bson import ObjectId
from app.v1.helper.json_encoder import JSONEncoder
from app.v1.errors import CustomFlaskErr as notice
from bson import ObjectId
from passlib.apps import custom_app_context as pwd_context
from app.v1.extensions.auth.jwt_auth import jwt, auth, confirm_email_jwt



def save_registration(data):
    print('save_registration...............')
    user = db.db.registration.find_one({'email':data['email']})

    '''if not validate_email(data['email'],verify=True,check_mx=True):
        raise notice(status_code=500,return_code=20006,action_status=False)'''
    
    
    if not data['password']  or  not data['email']:
        raise notice(status_code=422,return_code=20007,action_status=False)

    if not user :
        user=db.db.registration.insert({'email':data['email'],'FirstName':data['FirstName'],'LirstName':data['LastName'],'password':pwd_context.encrypt(data['password']),'JobPositionId':data['JobPositionId'],'image':data['image'],'deleted':0,'isActive':0,'role':'Admin','created_at':datetime.now(),'update_at':datetime.now(),'created_by':'root'})
        print('user',user)
        #email_confirm_token =  (user.generate_confirmation_token(data['email'],data['FirstName']))

        #confirm_url = (url_for('v1_blueprint.confirm',confirm_token=email_confirm_token,_external=True)) + '?email=' + data['email']

        # send confirm email to register user.
        #end_email(to=data['email'], subject='active',template='email_tpl/confirm',confirm_url=confirm_url,user=data['FirstName'],)
        return str(user)
        raise notice(status_code=200,return_code=30001,action_status=True,playbook={
                    'id':str(user),
                    'email': data['email'],
                    'create_time': datetime.now(),
        })
    else:
        raise notice(status_code=409,return_code=20004)


def login_registration(data):
        try:
            # Get user email and password.
            email, password = data.get('email').strip(), data.get('password').strip()

        except Exception as why:

            # Log input strip or etc. errors.
            # logging.info("Email or password is wrong. " + str(why))
            # Return invalid input error.
            return notice(status_code=422,return_code=20002)

        #if not validate_email(data['email'],verify=True,check_mx=True):
         #   raise error(status_code=500,return_code=20006)    

        # Check if user information is none.
        if email is None or password is None:
            raise notice(status_code=422,return_code=20002,action_status=False)

        # Get user if it is existed.
        user = db.db.registration.find_one({'email':email})
        print(user)
        # Check if user is not existed.
        if user is None:

            raise notice(status_code=404,return_code=20004,action_status=False)
        
        # Generate an access token if the password is correct.
        # Three roles for user, default user role is user.
        # user：0，admin:1, sa:2
        
        if user is not None and pwd_context.verify(password, user['password']):
            
            print(user['_id'])
            access_token=token = jwt.dumps({'email': email, 'role': user['role'],'_id':str(user['_id'])}).decode('ascii')

            

            # Generate refresh_token based on the user emamil.
            #refresh_token = (refresh_jwt.dumps({'email': email})).decode('ascii')
           
          
            return {
                '_id':str(user['_id']),
                "role": user['role'],
                "name":user['FirstName'],
                "access_token": access_token,
            }
           
        else:
            # Return invalid password
            raise notice(status_code=421,return_code=20003,action_status=False)

def data_registration(_id):
    attention=left=right=count=tot_time=0
    for data in db.db.registrationracker.find({"user_id":ObjectId(_id)},{'attention_percentage':1,'left_percentage':1,'right_percentage':1,'tot_time':1}):
        print(data)
        count=count+1
        attention=attention+data['attention_percentage']
        left=left+data['left_percentage']
        right=right+data['right_percentage']
        tot_time=tot_time+round(data['tot_time'])
    
    attention=round(attention/count)
    left=round(left/count)
    right=round(right/count)

    return jsonify({'attention':attention,'left':left,'right':right,'login':count,'time':tot_time})
