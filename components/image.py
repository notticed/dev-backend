from config import *
from tokens import *


app.mount("/uploads", StaticFiles(directory="./uploads"), name="uploads")

@app.post("/api/uploadFiles", tags=['image'])
def upload_files(files: List[UploadFile] = File(...)):
  links = []
  for file in files:
    if file.content_type in ['image/jpeg', 'image/jpg', 'image/png']:
      if file.size < 5000000:
        try:
          contents = file.file.read()
          with open(f'./uploads/{file.filename}', 'wb') as f:
            f.write(contents)
        except Exception:
          return {"message": "There was an error uploading the file(s)"}
        finally:
          file.file.close()
        links.append(f'http://localhost:8000/uploads/{file.filename}')
      else:
        return {'msg': 'Size of image is too big'}
    else:
      return {'msg': 'Upload only images'}
  return {"msg": f'Your iqmages were uploaded: {links}'}


@app.post('/api/uploadUrl', tags=['image'])
def upload_url(url, res: Response, req: Request):
  TOKENS = token.tokens_required(res, req)
  if TOKENS:
    random_string = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    img_source = requests.get(url).content
    with open(f'./uploads/{random_string}.jpg', 'wb') as handler:
      handler.write(img_source)
    return {'msg': f'Image was uploaded: http://localhost:8000/uploads/{random_string}.jpg'}
  return {"msg": 'You have to log in before'}




