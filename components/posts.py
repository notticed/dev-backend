from config import *
from payloads import post_payload
from schemes import Post
from tokens import *


crud_posts = CRUD(posts)
# crud_comments = CRUD(comments)

@app.post('/api/posts', tags=['posts'])
def create_post(post: Post, req: Request, res: Response):
  try:
    crud_posts.create(post_payload(token.tokens(res, req), post.title, post.content))
    return 'Post was published'
  except:
    return 'Something went wrong'

@app.delete('/api/posts', tags=['posts'])
def delete_post(post_id, req: Request, res: Response):
  if token.tokens(res, req) == str(crud_posts.get_id(post_id)['author']):
    crud_posts.delete(post_id)
    return 'Post was deleted'
  return 'You can not delete not yours post'


@app.patch('/api/post', tags=['posts'])
def update_post(post_id):
  pass

@app.post('/api/posts/like', tags=['posts'])
def like_post(req: Request, post_id, res: Response):
  try:
    return crud_posts.like(token.tokens(res, req), post_id)
  except: 
    return 'Something went wrong'

@app.post('/api/posts/dislike', tags=['posts'])
def dislike_post(req: Request, post_id, res: Response):
  try:
    return crud_posts.dislike(token.tokens(res, req), post_id)
  except: 
    return 'Something went wrong'


@app.get('/api/posts/{post_id}', tags=['posts'])
async def post_id(post_id):
  try:
    return crud_posts.get_id(post_id)
  except:
    return'Post not found'