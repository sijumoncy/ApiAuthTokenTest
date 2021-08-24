"""Auth related """
from os import name
from fastapi.exceptions import HTTPException
from sqlalchemy.sql.functions import user
from models import User
from auth import AuthHandler
import requests
import json

auth_handler = AuthHandler()

def user_register_kratos(register_details):
    """user registration kratos"""
    email = register_details.email
    password = register_details.password
    firstname = register_details.firstname
    lastname = register_details.lastname

    reg_flow = requests.get("http://127.0.0.1:4433/self-service/registration/api")
    if reg_flow.status_code == 200:
        flow_res = json.loads(reg_flow.content)
        reg_flow_id = flow_res["ui"]["action"]

        reg_data = {"traits.email": email,
                     "traits.name.first": firstname,
                     "traits.name.last": lastname,  
                     "password": password,
                     "method": "password"}
        headers = {}
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        reg_req = requests.post(reg_flow_id,headers=headers,json=reg_data)
        reg_response = json.loads(reg_req.content)
        if reg_req.status_code == 200:
            name_path = reg_response["identity"]["traits"]["name"]
            data={
                "details":"Registration Successfull",
                "registered_detials":{
                    "id":reg_response["identity"]["id"],
                    "email":reg_response["identity"]["traits"]["email"],
                    "Name":str(name_path["first"]) + " " + str(name_path["last"]) 
                },
                "token":reg_response["session_token"]
            }
            return data
        elif reg_req.status_code == 400:
            raise HTTPException(status_code=reg_req.status_code, detail=reg_response["ui"]["messages"][0]["text"])

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
            #print(session_id)
            print(login_req)
            return data
        else:
            raise HTTPException(status_code=401, detail="Invalid Credential")