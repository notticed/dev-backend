"""The main file for relate in blog"""
from config import *
from tokens import *


@app.post('/api/follow', tags=['relate'])
def follow(author_id, req: Request, res: Response):
  TOKEN = token.tokens_required(res, req)
  author_payload = subs.find_one({'author': author_id})

  if TOKEN and author_payload:
    follower_payload = subs.find_one({'author': TOKEN['access']})

    author_followers = author_payload['followers']
    follower_subscribers = follower_payload['subscribers']
    
    if TOKEN['access'] not in author_followers:
      author_followers.append(TOKEN['access'])
      follower_subscribers.append(author_id)
      subs.update_one({'author': str(author_payload['author'])}, { "$set": { 'followers': author_followers } }, upsert=False) 
      subs.update_one({'author': str(TOKEN['access'])}, { "$set": { 'subscribers': follower_subscribers } }, upsert=False)  
      return {'msg': 'You followed'}
    elif TOKEN['access'] in author_followers:
      author_followers.remove(TOKEN['access'])
      follower_subscribers.remove(author_id)
      subs.update_one({'author': str(author_payload['author'])}, { "$set": { 'followers': author_followers } }, upsert=False) 
      subs.update_one({'author': str(TOKEN['access'])}, { "$set": { 'subscribers': follower_subscribers } }, upsert=False)  
      return {'msg': 'You unfollowed'}
    else:
      return {'msg': 'Something went wrong'}
  return {'msg': 'Something went wrong'}


@app.get('/api/follow', tags=['relate'])
def followers(author_id):
  try:
    res = subs.find_one({'author': author_id})
    res['_id'] = str(res['_id'])
    return res
  except:
    return {'msg': 'Something went wrong'}



