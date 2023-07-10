from config import *
crud_info = CRUD(info)

def user_payload(fname, lname, nick, email, password):
  user = {
    'fname': fname,
    'lname': lname, 
    'nick': nick,
    'email': email, 
    'password': hashing(password),
    'photo': '',
  }
  return user

def post_payload(author_id, title, block: list):
  post = {
    "author": author_id,
    'date': datetime.now().isoformat(),
    'title': title,
    'block': block,
    'likes': 0,
    'dislikes': 0,
    'views': 0
  }
  return post

def comment_payload(author_id, post_id, content):
  comment = {
    'author': author_id,
    'post': post_id,
    'date': str(datetime.now()).split(' ')[0],
    'content': content,
    'likes': 0,
    'dislikes': 0,
    'thread': []
  }
  return comment

def relate_payload(author_id):
  follower = {
    'author': author_id,
    'followers': [],
    'subscribers': []
  }
  return follower


def info_payload(obj_id):
  info = {
    '_id': ObjectId(obj_id),
    'likes': [],
    'dislikes': [],
    'views': []
  }
  return info

