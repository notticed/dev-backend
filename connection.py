# the connection was copied from mongo docs
from pymongo import MongoClient
from bson.objectid import ObjectId
uri = "mongodb+srv://sample:Poher_123@cluster0.zcsjtwf.mongodb.net/"
client = MongoClient(uri)
db = client['sample_mflix']

# collections
users = db['users']
posts = db['posts']
comments = db['comments']
subs = db['subs']
# more info about posts and comments: likes/dislikes, views
info = db['info']
