from jose import jwt,JWTError
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from datetime import datetime,timedelta

class AuthHandler():
    """Authentication class"""
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
    secret = "SECRET"

    def get_hash_password(self,password):
        """hash password"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_pwd, hashed_pwd):
        """verify the password"""
        return self.pwd_context.verify(plain_pwd, hashed_pwd)

    def encode_token(self, user_id):
        """generate token"""
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm= ALGORITHMS.HS256
        )

    def decode_token(self, token):
        "decode and verify the token"
        """try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature Expired")
        except JWTError. as e:
            raise HTTPException(status_code=401, detail="Invalid Token")"""
        try:    
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']    
        except JWTError as e:
            raise HTTPException(status_code=401, detail=str(e))

    async def auth_wrapper(self, auth:HTTPAuthorizationCredentials = Security(security)):
        """authentication"""
        return self.decode_token(auth.credentials)
