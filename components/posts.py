from config import *
from payloads import post_payload, info_payload
from schemes import Post
from tokens import *


crud_posts = CRUD(posts)
crud_info = CRUD(info)
# crud_comments = CRUD(comments)

@app.post('/api/posts', tags=['posts'])
def create_post(post: Post, req: Request, res: Response):
  token.tokens(res, req)
  try:
    new_post = crud_posts.create(post_payload(token.tokens(res, req), post.title, post.content))
    crud_info.create(info_payload(new_post['_id']))
    return 'Post was published'
  except:
    return 'Something went wrong'

@app.delete('/api/posts', tags=['posts'])
def delete_post(post_id, req: Request, res: Response):
  if token.tokens(res, req) == str(crud_posts.get_id(post_id)['author']):
    crud_posts.delete(post_id)
    crud_info.delete(post_id)
    return 'Post was deleted'
  return 'You can not delete not yours post'


@app.patch('/api/post', tags=['posts'])
def update_post(post_id):
  pass

@app.post('/api/post/like', tags=['posts'])
def like(obj_id, res: Response, req: Request):
  crud_info.like(token.tokens(res, req), obj_id)
  crud_posts.update(obj_id, {'likes': len(crud_info.get_id(obj_id)['likes'])})
  crud_posts.update(obj_id, {'dislikes': len(crud_info.get_id(obj_id)['dislikes'])})
  return 'OK'

@app.post('/api/post/dislike', tags=['posts'])
def dislike(obj_id, res: Response, req: Request):
  crud_info.dislike(token.tokens(res, req), obj_id)
  crud_posts.update(obj_id, {'likes': len(crud_info.get_id(obj_id)['likes'])})
  crud_posts.update(obj_id, {'dislikes': len(crud_info.get_id(obj_id)['dislikes'])})
  return 'OK'


@app.get('/api/posts/{post_id}', tags=['posts'])
def post_id(post_id, res: Response, req: Request):
  tokens = token.tokens(res, req)
  try:
    crud_info._views(post_id, tokens)
    crud_posts.update(post_id, {'views': len(crud_info.get_id(post_id)['views'])})
    return crud_posts.get_id(post_id)
  except:
    return'Post not found'
  

