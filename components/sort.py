"""
The sort module 

1. search - search query 
http://www.site.com/?search=43240234
The support items of search types:
a. Id 
b. Title (posts)
c. Content

2. sortBy - sort type (default: date_day)
http://www.site.com/?searchBy=popular_by_day
The support items of sortBy types:
  1. Popular
    a. popular_by_year
    b. popular_by_month
    c. popular_by_week
    d. popular_by_day
  2. Date (from newest to oldest)
    a. date_year
    b. date_month
    c. date_week
    d. date_day

3. limit - limit of pages (default: 20)
http://www.site.com/?limit=20
Random number from 20 to 100 is supported to page query parameter

4. page - number of page
http://www.site.com/?page=3
Random number from 1 to lenght of list with data 1 > x > infinity


"""
from config import *
import pymongo


now_time = str(datetime.now()).split(" ")[0].split("-")
now_time_iso = datetime.now().isoformat()


query_params = {"search": (str, ''), "sortBy": (str, 'all_time'), "page": (int, 1), "limit": (int, 20)}
query_model = create_model("Query", **query_params)

def convert_data(db):
    data = []
    for to_str in db:
      to_str['_id'] = str(to_str['_id'])
      data.append(to_str)
    return data

# the main class with sort methods
class Sort:
  def __init__(self, db, params):
    self.db_type = str(db)
    self.db = eval(db)
    self.search = params['search']
    self.sortBy = params['sortBy']
    self.page = params['page']
    self.limit = params['limit']
    # the list with output data
    self.data = convert_data(self.db.find())
  
      # self.data = convert_data(self.db.find({ "$text": { "$search": // } }).sort('date', pymongo.ASCENDING))

  def sortPosts(self):
    sortDate = {
      # by date
      'all_time': {'$gt': f'1600-01-01T00:00:00.000000', '$lt': f'3000-01-01T00:00:00.000000'},
      'date_year': {'$gt': f'{now_time[0]}-01-01T00:00:00.000000', '$lt': now_time_iso},
      'date_month': {'$gt': f'{now_time[0]}-{now_time[1]}-01T00:00:00.000000', '$lt': now_time_iso},
      'date_day': {'$gt': f'{now_time[0]}-{now_time[1]}-{now_time[2]}T00:00:00.000000', '$lt': now_time_iso},

    } 
    sortPopular = {
      'popular_day': sorted(convert_data(self.db.find({'date': sortDate['date_day']})), key=lambda item: item['views'], reverse=True),
      'popular_month': sorted(convert_data(self.db.find({'date': sortDate['date_month']})), key=lambda item: item['views'], reverse=True),
      'popular_year': sorted(convert_data(self.db.find({'date': sortDate['date_year']})), key=lambda item: item['views'], reverse=True),
      'popular': sorted(self.data, key=lambda item: item['views'], reverse=True),
    }
    self.db.create_index([('title' , pymongo.TEXT), ('content' , pymongo.TEXT), ('date', pymongo.TEXT), ('views', pymongo.TEXT)])
    
    if self.sortBy in sortDate.keys():
      self.data = convert_data(self.db.find({
          '$and': [
            {'$or': [
              { "title": { "$regex": self.search, '$options': 'i' } },
              { "content": { "$regex": self.search, '$options': 'i' } }
            ]},
            {'date': sortDate[self.sortBy]},
          ]
        }))
    else:
      self.data = sortPopular[self.sortBy]
    

    # the final list with results
    data = []
    for n in range(0, math.ceil(len(self.data)/self.limit)):
      data.append(list(self.data[0:self.limit]))
      del self.data[0:self.limit]
    self.data = data
  
    try:
      return self.data[self.page-1]
    except:
      return'Page not found'
    
  
  
  def sortUsers(self):
    self.db.create_index([('nick' , pymongo.TEXT)])
    if len(self.search):
      self.data = convert_data(self.db.find({ "nick": { "$regex": f"^{self.search}" } }))
    
    data = []
    for n in range(0, math.ceil(len(self.data)/self.limit)):
      data.append(list(self.data[0:self.limit]))
      del self.data[0:self.limit]
    self.data = data
    try:
      return self.data[self.page-1]
    except:
      return'Page not found'


  def get_sort(self):
    if self.db_type == 'users':
      return self.sortUsers()
    elif self.db_type == 'posts':
      return self.sortPosts()
    elif self.db_type == 'comments':
      pass  
    else:
      return []

@app.get('/api/{db}', tags=['sort'])
async def all(db: str, res: Response, params: query_model = Depends()):
  sort = Sort(db, params.dict())
  number = len(sort.data)
  res.set_cookie(
    key='number',
    value=number
  )
  return sort.get_sort()


