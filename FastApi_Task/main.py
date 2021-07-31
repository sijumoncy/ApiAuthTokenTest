from sqlalchemy.orm.session import Session
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
from scripts.auth_scripts import register_user,user_login

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
    return {"msg":"Welcome to the API Portal"}


#auth 
@app.post('/register')
async def register(auth_details:schemas.AuthDetails):
    """register user"""
    data = register_user(auth_details, session)
    return data

@app.post('/login')
def login(auth_details:schemas.AuthDetails):
    """user login"""
    data = user_login(auth_details, session)
    return data

#handle upload files
@app.post("/upload-text-file")
async def uploadfiles( langauage:str , file:UploadFile = File(...),\
    username = Depends(auth_handler.auth_wrapper)):
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
    return {"DBstatus": "Success" ,"info": f"file '{file.filename}' saved at '{file_location}' type '{file.content_type}' language '{lan} "}


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




'''
#Functions for adding keywords with duplicate entry restrict
tempararily add this functionality along with ml-db entry function
keywordadd(session)
'''



