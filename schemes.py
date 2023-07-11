from config import *

# Scheme for registration
class Registration(BaseModel):
  fname: str
  lname: str
  nick: str
  email: str
  password: str

# Scheme for login
class Login(BaseModel):
  nick: str
  password: str

# Scheme for post
class Post(BaseModel):
  title: str
  content: str


# Scheme for comment
class Comment(BaseModel):
  content: str


