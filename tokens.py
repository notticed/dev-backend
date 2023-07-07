# The token module 
from config import *
import time
import jwt
from jwt.exceptions import ExpiredSignatureError

# JWT token config
ACCESS_TOKEN_EXPIRE_DELTA = 10.0
REFRESH_TOKEN_EXPIRE_DELTA = 2592000.0
SECRET_KEY = 'secret'
ALGORITHM = 'HS256'

class Token():

  def auth_token(self, res, req):
    access_token = req.cookies.get('access_token_cookie')
    refresh_token = req.cookies.get('refresh_token_cookie')

    if access_token and refresh_token:
      raise HTTPException(status_code=403, detail='You already logged in')
    self.tokenAccess(access_token, res),
    self.tokenRefresh(refresh_token, res)

  def tokens(self, res, req):
    access_token = req.cookies.get('access_token_cookie')
    refresh_token = req.cookies.get('refresh_token_cookie')
    
      
    if not access_token and not refresh_token:
      raise HTTPException(status_code=401, detail='You have to sign in before')
    
    tokens = {
      'access': self.tokenAccess(access_token, res)['user_id'],
      'refresh': self.tokenRefresh(refresh_token, res)
    }
    return tokens['access']

  # return access_token
  def create_access_token(self, user_id):
    access_token = jwt.encode({
      'user_id': user_id,
      'exp': time.time() + ACCESS_TOKEN_EXPIRE_DELTA
    }, SECRET_KEY, algorithm=ALGORITHM)
    return access_token
  
  # return refresh_token
  def create_refresh_token(self):
    refresh_token = jwt.encode({
      'exp': time.time() + REFRESH_TOKEN_EXPIRE_DELTA
    }, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token
  
  def tokenRefresh(self, refresh_token, res):
    if refresh_token:
      try:
        return jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
      except ExpiredSignatureError:
        new_refresh_token = self.create_refresh_token()
        res.set_cookie(key="refresh_token_cookie", value=new_refresh_token)
        return jwt.decode(new_refresh_token, SECRET_KEY, algorithms=ALGORITHM)

    
  def tokenAccess(self, access_token, res):
    if access_token:
      try:
        return jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
      except ExpiredSignatureError:
        tokenSplit = access_token.split(".")
        payload = json.loads((base64.b64decode(str(tokenSplit[1]) + "==")).decode("utf-8"))
        new_access_token = self.create_access_token(payload['user_id'])
        res.set_cookie(key="access_token_cookie", value=new_access_token)
        return jwt.decode(new_access_token, SECRET_KEY, algorithms=ALGORITHM)
token = Token()