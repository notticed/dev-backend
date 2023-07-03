from config import *
from tokens import *

crud_users = CRUD(users)

# @app.delete('/api/user', tags=['user'])
# def delete_user(user_id, res: Response, req: Request):
#   TOKENS = token.tokens_required(res, req)
#   if TOKENS and TOKENS['access']== id:
#     return crud_users.delete({'_id': ObjectId(user_id)})
#   return {'msg': 'You do not have permission for this'}

@app.get('/api/user', tags=['user'])
def all_users():
  return crud_users.get_all()

@app.get('/api/@{nick}', tags=['user'])
def user_nick(nick):
  try:
    result = users.find_one({'nick': nick})
    result["_id"] = str(result["_id"])
    return result
  except:
    return "User not found"

