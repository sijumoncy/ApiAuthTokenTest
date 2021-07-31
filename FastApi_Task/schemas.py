from pydantic import BaseModel

class AuthDetails(BaseModel):
    """schema for authentication"""
    username:str
    password:str