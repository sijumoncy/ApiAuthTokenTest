"""Auth related """
from fastapi.exceptions import HTTPException
from sqlalchemy.sql.functions import user
from models import User
from auth import AuthHandler

auth_handler = AuthHandler()

current_user = None

def register_user(auth_details, session):
    """register user"""
    username = auth_details.username
    password =  auth_details.password
    data = {"details":""}

    db_user =  session.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username Already registered")
    else:
        hashed_pwd = auth_handler.get_hash_password(password=password)
        new_entry = User(
                   username = username,
                   hashed_pass = hashed_pwd
                )

        session.add(new_entry)
        session.commit()
        data["details"] = "Registration Success"
        return data

def user_login(auth_details, session):
    """user login"""
    username = auth_details.username
    password =  auth_details.password
    data = {"details":"","token":""}

    db_user =  session.query(User).filter(User.username == username).first()
    if db_user:
        if auth_handler.verify_password(plain_pwd=password,\
            hashed_pwd=db_user.hashed_pass):
            token = auth_handler.encode_token(db_user.username)
            data["details"] = "Login Succesfull"
            data["token"] = token

        else:
            raise HTTPException(status_code=401, detail="Invalid Credentials, Login Failed")
    else:
            raise HTTPException(status_code=401, detail="No such user exist, Register First")
    return data