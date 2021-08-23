"""Auth related """
from fastapi.exceptions import HTTPException
from sqlalchemy.sql.functions import user
from models import User
from auth import AuthHandler


import requests
import json

auth_handler = AuthHandler()

current_user = None

# def register_user(auth_details, session):
#     """register user"""
#     username = auth_details.username
#     password =  auth_details.password
#     data = {"details":""}

#     db_user =  session.query(User).filter(User.username == username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username Already registered")
#     else:
#         hashed_pwd = auth_handler.get_hash_password(password=password)
#         new_entry = User(
#                    username = username,
#                    hashed_pass = hashed_pwd
#                 )

#         session.add(new_entry)
#         session.commit()
#         data["details"] = "Registration Success"
#         return data

# def user_login(auth_details, session):
#     """user login"""
#     username = auth_details.username
#     password =  auth_details.password
#     data = {"details":"","token":""}

#     db_user =  session.query(User).filter(User.username == username).first()
#     if db_user:
#         if auth_handler.verify_password(plain_pwd=password,\
#             hashed_pwd=db_user.hashed_pass):
#             token = auth_handler.encode_token(db_user.username)
#             data["details"] = "Login Succesfull"
#             data["token"] = token

#         else:
#             raise HTTPException(status_code=401, detail="Invalid Credentials, Login Failed")
#     else:
#             raise HTTPException(status_code=401, detail="No such user exist, Register First")
#     return data

def user_login_kratos(auth_details):
    "kratos login"
    username = auth_details.username
    password =  auth_details.password
    data = {"details":"","token":""}

    flow_res = requests.get("http://127.0.0.1:4433/self-service/login/api")
    if flow_res.status_code == 200:
        flow_res = json.loads(flow_res.content)
        flow_id = flow_res["ui"]["action"]

        cred_data = {"password_identifier": username, "password": password, "method": "password"}
        login_req = requests.post(flow_id, json=cred_data)
        if login_req.status_code == 200:
            login_req = json.loads(login_req.content)
            session_id = login_req["session_token"]
            data["details"] = "Login Succesfull"
            data["token"] = session_id
            return data
        else:
            raise HTTPException(status_code=401, detail="Invalid Credential")