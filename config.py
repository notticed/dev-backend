# import all necessary libraries for project
from fastapi import FastAPI, Depends, Request, Response, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
# from fastapi_jwt_auth.exceptions import (
#     InvalidHeaderError,
#     CSRFError,
#     JWTDecodeError,
#     RevokedTokenError,
#     MissingTokenError,
#     AccessTokenRequired,
#     RefreshTokenRequired,
#     FreshTokenRequired
# )
from pydantic import BaseModel, create_model
from connection import *
from fastapi.middleware.cors import CORSMiddleware
from hashing import *
from bson.objectid import ObjectId
from typing import Optional, List
from datetime import *
import random
import string
import math
import json
import base64
import requests


# init the main FastAPI class
app = FastAPI()

# cors policy
origins = ""
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = origins
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# the main CRUD class for DB
class CRUD:
  def __init__(self, collection):
    self.collection = collection
    
  def create(self, scheme): 
    try:
      self.collection.insert_one(scheme)
      return self.collection.find_one(scheme)
    except:
      return False

  def delete(self, id):
    try:
      self.collection.delete_one({'_id': ObjectId(id)})
      return True
    except:
      return False

  def update(self, id, value):
    try:
      self.collection.update_one({'_id': ObjectId(id)}, {"$set": value}, upsert=False)
      return True
    except:
      return False
    
  def get_all(self):
    try:
      all = []
      for item in self.collection.find():
        item['_id'] = str(item['_id'])
        all.append(item)
      return all
    except:
      return None
    
  def get_id(self, id):
    try: 
      result_id = self.collection.find_one({'_id': ObjectId(id)})
      result_id['_id'] = str(result_id['_id'])
      return result_id
    except: 
      return'Not found'
    
  def like(self, user_id, obj_id):
    try:
      if user_id not in self.get_id(obj_id)['likes']:
        likes = self.get_id(obj_id)['likes']
        dislikes = self.get_id(obj_id)['dislikes']
        try:
          dislikes.remove(user_id)
          self.update(obj_id, {'dislikes': dislikes})
        except:
          pass
        likes.append(user_id)
        self.update(obj_id, {'likes': likes})
        return 'Like was set'
      else:
        likes = self.get_id(obj_id)['likes']
        likes.remove(user_id)
        self.update(obj_id, {'likes': likes})
        return 'Like was deleted'
    except:
      return 'Something went wrong'


  def dislike(self, user_id, obj_id):
    try:
      if user_id not in self.get_id(obj_id)['dislikes']:
        dislikes = self.get_id(obj_id)['dislikes']
        likes = self.get_id(obj_id)['likes']
        try:
          likes.remove(user_id)
          self.update(obj_id, {'likes': likes})
        except:
          pass
        dislikes.append(user_id)
        self.update(obj_id, {'dislikes': dislikes})
        return 'Dislike was set'
      else:
        dislikes = self.get_id(obj_id)['dislikes']
        dislikes.remove(user_id)
        self.update(obj_id, {'dislikes': dislikes})
        return 'Dislike was deleted'
    except:
      return 'Something went wrong'


# AuthJWT class settings
class Settings(BaseModel):
  authjwt_secret_key: str = "secret"
  authjwt_token_location: set = {"cookies"}
  authjwt_cookie_csrf_protect: bool = False

@AuthJWT.load_config
def get_config():
  return Settings()

# error handler
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
  return JSONResponse(
    status_code=exc.status_code,
    content={"detail": exc.message}
  )

