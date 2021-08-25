from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import false, true
from database import engine
from models import metadata,Base
from sqlalchemy.orm import sessionmaker
from scripts.inputconvert import texttojson
from scripts.adddbdata import dbentry,keywordadd
from scripts.getbook import fetchbook,fetchverse,fetchword,randomword
import json
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
#auth section
from auth import AuthHandler
import schemas
from scripts.auth_scripts import user_login_kratos,user_register_kratos,user_role_add

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)  
session = Session()

auth_handler = AuthHandler()



app = FastAPI(title="Book API with Auth")
destination_path = r"inputfiles"

#cross origin resource sharing permissions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"msg":"Welcome to the API Portal with Kratos"}

@app.post('/register')
def register(register_details:schemas.Registration):
    """user register"""
    data = user_register_kratos(register_details)
    return data
    
@app.post('/login')
def login(auth_details:schemas.AuthDetails):
    """user login"""
    data = user_login_kratos(auth_details)
    return data

@app.post('/logout')
def logout(message = Depends(auth_handler.kratos_logout)):
    """user logout"""
    return message

@app.post('/userrole')
def userrole(role_data:schemas.userrole):
    """Update User Roles
        User roles should provide in an ARRAY -
        Array values will overwrite the exisitng array of roles -
        No roles will be allocated on registration , will be consider as a normal user -
        avaialable roles are 
        ["SuperAdmin", "VachanAdmin" ,"AgMTTranslator","AgMTProjectOwner"]
    """
    user_id = role_data.userid
    role_list = role_data.roles
    data=user_role_add(user_id,role_list)
    return data

#handle upload files
@app.post("/upload-text-file")
async def uploadfiles( langauage:str , file:UploadFile = File(...),\
    roles = Depends(auth_handler.kratos_session_validation)):


    #Demo check for user roles based access
    bible_upload_roles = ["SuperAdmin","VachanAdmin"]
    permision = False
    for role in roles:
        if role in bible_upload_roles:
           permision = True      
    if permision:
        lan = langauage.capitalize()
        file_name = file.filename
        file_location = f"files/{file_name}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        if file_name.endswith(".txt"):
            jsonobj = texttojson(file_name)
            dbentry(jsonobj, session, lan)
        elif file_name.endswith(".json"):
            with open(file_location) as json_file:
                enjson = json.load(json_file)
            dbentry(enjson, session, lan)                 
        return {"status": "Success" ,"info": f"file '{file.filename}' saved at '{file_location}' type '{file.content_type}' language '{lan} "}

    else:
        return {"status":"Not uploaded.. Permission Denied"}

#fetch books chapter wise
@app.get("/getbook")
async def getbook(bookcode : str, chapter : int , language_code: str):
    data = fetchbook(bookcode,chapter,language_code,session)
    return data

#fetch verse
@app.get("/fetchverse")
async def getverse(bookcode:str , chapter:int , verse_number: int, language_code: str ):
    data = fetchverse(bookcode,chapter,language_code,verse_number,session)
    return data

#special word search
@app.get("/specialwordsearch")
async def getword(word:str):
    data = fetchword(word,session)
    return data 


#random word finidng
@app.get("/randomwordsearch")
async def randomsearch(word:str, language:str):
    data = randomword(word,session,language)
    return data



