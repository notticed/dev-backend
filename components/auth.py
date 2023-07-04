"""
Auth component module

File contains 3 methods: 
1.Login
2.Registration
3.Logout

users - collection with users in database

"""

from config import *  # config data
from schemes import Login, Registration # import schemas
from tokens import * # import Token class
from payloads import * # import payloads schemas


# instance of CRUD class
crud_security = CRUD(users)
crud_relate = CRUD(subs)

# LOGIN METHOD
@app.post('/api/login', tags=['auth'])
def login(login: Login, req: Request, res: Response):

  """
  The login method take the data from Login scheme and then compare this data with data in database,
  after this send a response with tokens or with errors
  """

  # check for tokens
  if not token.tokens_required(res, req):
    # get user_indentity from database
    payload = users.find_one({'nick': login.nick})

    # check the user in database
    if payload and check_hashing(login.password, payload['password']):

      # create tokens and throw them to the cookie
      res.set_cookie(key="access_token_cookie", value=token.create_access_token(str(payload['_id'])))
      res.set_cookie(key="refresh_token_cookie", value=token.create_refresh_token())

      return {"msg": "Successfull logged in"}
    
    return {'msg': 'Login or password is incorrect'}
  
  return {'msg': 'You are already logged in'}

# LOGOUT METHOD
@app.get('/api/logout', tags=['auth'])
def logout (Authorize: AuthJWT = Depends()):

  """
  The simplest method in this file. Just unset tokens from cookies and that's all.
  """

  Authorize.unset_jwt_cookies()
  return {"msg": "Tokens have been deleted"}


# REGISTRATION METHOD
@app.post('/api/register', tags=['auth'])
def register(req:Request, user: Registration, res: Response):

  """
  The registration method collect user data from registration form and then create a new user in database
  """

  # check for tokens
  if not token.tokens_required(res, req):

    # check step-by-step: email first, and then nick. On each step might throw the neccessary error.
    # check for no same email
    if users.find_one({'email': user.email}) == None:
      
      # check for no same nick
      if users.find_one({'nick': user.nick}) == None:
        
        # collect user_identity from scheme

        # use CRUD method to create a new user in database
        payload = crud_security.create(user_payload(user.fname, user.lname, user.nick, user.email, user.password))

        # create tokens and throw them to the cookies
        res.set_cookie(key="access_token_cookie", value=token.create_access_token(str(payload['_id'])))
        res.set_cookie(key="refresh_token_cookie", value=token.create_refresh_token())
      
        crud_relate.create(relate_payload(str(payload['_id'])))

        return {"msg": "Successful registration"}
      
      return {'msg': 'Nickname already exists'}
    
    return {'msg': 'Email already exists'}
  

