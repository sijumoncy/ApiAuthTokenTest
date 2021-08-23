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

    # def get_hash_password(self,password):
    #     """hash password"""
    #     return self.pwd_context.hash(password)

    # def verify_password(self, plain_pwd, hashed_pwd):
    #     """verify the password"""
    #     return self.pwd_context.verify(plain_pwd, hashed_pwd)

    # def encode_token(self, user_id):
    #     """generate token"""
    #     payload = {
    #         'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
    #         'iat': datetime.utcnow(),
    #         'sub': user_id
    #     }
    #     return jwt.encode(
    #         payload,
    #         self.secret,
    #         algorithm= ALGORITHMS.HS256
    #     )

    # def decode_token(self, token):
    #     "decode and verify the token"
    #     """try:
    #         payload = jwt.decode(token, self.secret, algorithms=['HS256'])
    #         return payload['sub']
    #     except jwt.ExpiredSignatureError:
    #         raise HTTPException(status_code=401, detail="Signature Expired")
    #     except JWTError. as e:
    #         raise HTTPException(status_code=401, detail="Invalid Token")"""
    #     try:    
    #         payload = jwt.decode(token, self.secret, algorithms=['HS256'])
    #         return payload['sub']
    #     except JWTError as e:
    #         raise HTTPException(status_code=401, detail=str(e))

    # async def auth_wrapper(self, auth:HTTPAuthorizationCredentials = Security(security)):
    #     """authentication"""
    #     return self.decode_token(auth.credentials)

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
            print(data)
            return data

        elif user_data.status_code == 401:
            print(data)
            raise HTTPException(status_code=401, detail=data["error"])

        elif user_data.status_code == 500:
            print(data)
            raise HTTPException(status_code=500, detail=data["error"])

    # def kratos_logout(self,auth:HTTPAuthorizationCredentials):
    #     recieve_token = auth.credentials
    #     url = "http://127.0.0.1:4433//sessions"
    #     payload = {"session_token": recieve_token}
    #     headers = {}
    #     headers["Content-Type"] = "application/json"
    #     response = requests.request("DELETE", url, headers=headers, data=payload)
    #     data = json.loads(response.content)
    #     if response.status_code == 204:
    #         return data
    #     elif response.status_code == 400:
    #         raise HTTPException(status_code=401, detail=data["error"])
    #     elif response.status_code == 500:
    #         print(data)
    #         raise HTTPException(status_code=500, detail=data["error"])