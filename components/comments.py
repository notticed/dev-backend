from config import *
from tokens import *
from schemes import *
from payloads import comment_payload
crud_comments = CRUD(comments)


@app.post('/api/comment', tags=['comments'])
def create_comment(comment: Comment, req: Request, res: Response, post_id):
  TOKENS = token.tokens_required(res, req)
  if TOKENS:
    try:
      crud_comments.create(comment_payload(TOKENS['access'], post_id, comment.content))
      return {'msg': 'Comment was published'}
    except:
      return {"msg": "Something went wrong"}
  return {"msg": 'You have logged in before'}
  
@app.delete('/api/comment', tags=['comments'])
def delete_comment(req: Request, comment_id, res: Response):
  TOKENS = token.tokens_required(res, req)
  if TOKENS and TOKENS['access'] == str(crud_comments.get_id(comment_id)['_id']):
    try:
      crud_comments.delete(comment_id)
      return {'msg': 'Comment was deleted'}
    except:
      return {'msg':'Something went wrong'}

@app.patch('/api/comment', tags=['comments'])
def update_comment(req: Request, post_id, Authorize: AuthJWT = Depends()):
  pass

@app.get('/api/comment', tags=['comments'])
def all_comments():
  return crud_comments.get_all()

@app.post('/api/comment/like', tags=['comments'])
def like_comment(req: Request, comment_id, res: Response):
  TOKENS = token.tokens_required(res, req)
  if TOKENS:
    try:
      return crud_comments.like(TOKENS['access'], comment_id)
    except: 
      return {'msg': 'Something went wrong'}
  return {'msg': 'Log in before'}
  
@app.post('/api/comment/dislike', tags=['comments'])
def dislike_comment(req: Request, comment_id, res: Response):
  TOKENS = token.tokens_required(res, req)
  if TOKENS:
    try:
      return crud_comments.dislike(TOKENS['access'], comment_id)
    except: 
      return {'msg': 'Something went wrong'}
  return {'msg': 'Log in before'}
  
@app.get('/api/comment/post_id', tags=['comments'])
def comment_by_post(post_id):
  comments = []
  for n in crud_comments.get_all():
    if n['post'] == post_id:
      comments.append(n)
  return comments


@app.post('/api/comment/reply', tags=['comments'])
def reply(comment_id, res: Response, req: Request, comment: Comment):
  TOKENS = token.tokens_required(res, req)
  thread_comment = crud_comments.get_id(comment_id)

  if TOKENS:
    threads = thread_comment['thread']
    threads.append(comment_payload(TOKENS['access'], '', comment.content))
    crud_comments.update(comment_id, {'thread': threads})
    return {"msg": "Reply was published"}
  return {"msg": "You have logged in before"}

