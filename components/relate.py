"""The main file for relate in blog"""
from config import *
from tokens import *


@app.post('/api/follow', tags=['relate'])
def follow(author_id, req: Request, res: Response):
  author_payload = subs.find_one({'author': author_id})

  if author_payload:
    follower_payload = subs.find_one({'author': token.tokens(res, req)})

    author_followers = author_payload['followers']
    follower_subscribers = follower_payload['subscribers']
    
    if token.tokens(res, req) not in author_followers:
      author_followers.append(token.tokens(res, req))
      follower_subscribers.append(author_id)
      subs.update_one({'author': str(author_payload['author'])}, { "$set": { 'followers': author_followers } }, upsert=False) 
      subs.update_one({'author': str(token.tokens(res, req))}, { "$set": { 'subscribers': follower_subscribers } }, upsert=False)  
      return 'You followed'
    elif token.tokens(res, req) in author_followers:
      author_followers.remove(token.tokens(res, req))
      follower_subscribers.remove(author_id)
      subs.update_one({'author': str(author_payload['author'])}, { "$set": { 'followers': author_followers } }, upsert=False) 
      subs.update_one({'author': str(token.tokens(res, req))}, { "$set": { 'subscribers': follower_subscribers } }, upsert=False)  
      return 'You unfollowed'
    else:
      return 'Something went wrong'
  else:
    return'Author not found'


@app.get('/api/follow', tags=['relate'])
def followers(author_id):
  try:
    res = subs.find_one({'author': author_id})
    res['_id'] = str(res['_id'])
    return res
  except:
    return 'Something went wrong'



