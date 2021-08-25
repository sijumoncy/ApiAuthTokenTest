from jose import jwt,JWTError
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from datetime import datetime,timedelta
import requests
import json


class AuthHandler():
    """Authentication class"""
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
    secret = "SECRET"


    def kratos_session_validation(self,auth:HTTPAuthorizationCredentials = Security(security)):
        """kratos session validity check"""
        recieve_token = auth.credentials
        user_url = "http://127.0.0.1:4433/sessions/whoami"
        headers = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {recieve_token}"

        user_data = requests.get(user_url, headers=headers)
        data = json.loads(user_data.content)

        if user_data.status_code == 200:
            if "userrole" in data["identity"]["traits"]:
                roles = data["identity"]["traits"]["userrole"]
                return roles
            else:
                return []    

        elif user_data.status_code == 401:
            raise HTTPException(status_code=401, detail=data["error"])

        elif user_data.status_code == 500:
            raise HTTPException(status_code=500, detail=data["error"])

    def kratos_logout(self,auth:HTTPAuthorizationCredentials= Security(security)):
        recieve_token = auth.credentials
        url = "http://127.0.0.1:4433/self-service/logout/api"
        payload = {"session_token": recieve_token}
        headers = {}
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        response = requests.delete(url, headers=headers, json=payload)
        if response.status_code == 204:
            data = {"message":"Successfully Logged out"}
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            raise HTTPException(status_code=401, detail=data["error"])
        elif response.status_code == 500:
            data = json.loads(response.content)
            raise HTTPException(status_code=500, detail=data["error"])
