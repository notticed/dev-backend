from config import *

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

def post_payload(author_id, title, content):
  post = {
    "author": author_id,
    'date': datetime.now().isoformat(),
    'title': title,
    'content': content,
    'likes': [],
    'dislikes': [],
    'views': 0,
  }
  return post

def comment_payload(author_id, post, content):
  comment = {
    'author': author_id,
    'post': post,
    'date': str(datetime.now()).split(' ')[0],
    'content': content,
    'likes': [],
    'dislikes': []
  }
  return comment

def relate_payload(author_id):
  follower = {
    'author': author_id,
    'followers': [],
    'subscribers': []
  }
  return follower
