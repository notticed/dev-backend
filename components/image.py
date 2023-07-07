from config import *
from tokens import *


app.mount("/uploads", StaticFiles(directory="./uploads"), name="uploads")

@app.post("/api/uploadFiles", tags=['image'])
def upload_files(req: Request, res: Response, files: List[UploadFile] = File(...)):
  token.tokens(res,  req)
  links = []
  for file in files:
    if file.content_type in ['image/jpeg', 'image/jpg', 'image/png']:
      if file.size < 5000000:
        try:
          contents = file.file.read()
          with open(f'./uploads/{file.filename}', 'wb') as f:
            f.write(contents)
        except Exception:
          return 'Something went wrong'
        finally:
          file.file.close()
        links.append(f'http://localhost:8000/uploads/{file.filename}')
      else:
        return 'Too big size of image'
    else:
      return 'Ivalid format of image'
  return {"msg": f'Your iqmages were uploaded: {links}'}


@app.post('/api/uploadUrl', tags=['image'])
def upload_url(url, res: Response, req: Request):
  token.tokens(res, req)
  try:
    random_string = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    img_source = requests.get(url).content
    with open(f'./uploads/{random_string}.jpg', 'wb') as handler:
      handler.write(img_source)
    return {'msg': f'Image was uploaded: http://localhost:8000/uploads/{random_string}.jpg'}
  except:
    return 'Too big size of image'






