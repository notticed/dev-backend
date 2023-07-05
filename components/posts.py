from config import *
from payloads import post_payload
from schemes import Post
from tokens import *


crud_posts = CRUD(posts)
# crud_comments = CRUD(comments)

@app.post('/api/posts', tags=['posts'])
def create_post(post: Post, req: Request, res: Response):
  TOKENS = token.tokens_required(res, req)
  if TOKENS:
    try:
      crud_posts.create(post_payload(TOKENS['access'], post.title, post.content))
      return {'msg': 'Post was published'}
    except:
      return {'msg': 'Something went wrong'}
  return {'msg': 'Log in before'}

@app.delete('/api/posts', tags=['posts'])
def delete_post(post_id, req: Request, res: Response):
  TOKENS = token.tokens_required(res, req)
  if TOKENS and TOKENS['access'] == str(crud_posts.get_id(post_id)['author']):
    try:
      crud_posts.delete(post_id)
      return {'msg': 'Post was deleted'}
    except:
      return {'msg': 'Something went wrong'}
  return {'msg': 'Log in before or you cannot delete the post'}

@app.patch('/api/post', tags=['posts'])
def update_post(post_id):
  pass

@app.post('/api/posts/like', tags=['posts'])
def like_post(req: Request, post_id, res: Response):
  TOKENS = token.tokens_required(res, req)
  if TOKENS:
    try:
      return crud_posts.like(TOKENS['access'], post_id)
    except: 
      return {'msg': 'Something went wrong'}
  return {'msg': 'Log in before'}

@app.post('/api/posts/dislike', tags=['posts'])
def dislike_post(req: Request, post_id, res: Response):
  TOKENS = token.tokens_required(res, req)
  if TOKENS:
    try:
      return crud_posts.dislike(TOKENS['access'], post_id)
    except:
      return {'msg': 'Something went wrong'}
  return {'msg': "Log in before"}


@app.get('/api/post/{post_id}', tags=['posts'])
async def post_id(post_id):
  try:
    return crud_posts.get_id(post_id)
  except:
    return "Post was not found"