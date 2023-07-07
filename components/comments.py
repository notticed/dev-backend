from config import *
from tokens import *
from schemes import *
from payloads import comment_payload


crud_comments = CRUD(comments)

@app.post('/api/comment', tags=['comments'])
def create_comment(comment: Comment, req: Request, res: Response, post_id):

  try:
    crud_comments.create(comment_payload(token.tokens(res, req), post_id, comment.content))
    return 'Comment was published'
  except:
    return 'Something went wrong'
  
@app.delete('/api/comment', tags=['comments'])
def delete_comment(req: Request, comment_id, res: Response):
  if token.tokens(res, req) == str(crud_comments.get_id(comment_id)['author']):
    try:
      crud_comments.delete(comment_id)
      return 'Comment was deleted'
    except:
      return 'Something went wrong'
  return 'You do not have permission for this'

@app.patch('/api/comment', tags=['comments'])
def update_comment(req: Request, post_id, Authorize: AuthJWT = Depends()):
  pass

@app.get('/api/comment', tags=['comments'])
def all_comments():
  return crud_comments.get_all()

@app.post('/api/comment/like', tags=['comments'])
def like_comment(req: Request, comment_id, res: Response):

  try:
    return crud_comments.like(token.tokens(res, req), comment_id)
  except: 
    return 'Something went wrong'

  
@app.post('/api/comment/dislike', tags=['comments'])
def dislike_comment(req: Request, comment_id, res: Response):

  try:
    return crud_comments.dislike(token.tokens(res, req), comment_id)
  except: 
    return 'Something went wrong'
  
@app.get('/api/comment/post_id', tags=['comments'])
def comment_by_post(post_id):
  comments = []
  for n in crud_comments.get_all():
    if n['post'] == post_id:
      comments.append(n)
  return comments


@app.post('/api/comment/reply', tags=['comments'])
def reply(comment_id, res: Response, req: Request, comment: Comment):

  thread_comment = crud_comments.get_id(comment_id)

  threads = thread_comment['thread']
  threads.append(comment_payload(token.tokens(res, req), '', comment.content))
  return 'Reply was published'

