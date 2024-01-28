from fastapi import FastAPI, UploadFile, File, Depends
from typing import List
from .database import engine
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get("/")
def index():
   return {"Hello World"}

@app.post("/upload")
def upload(files: List[UploadFile] = File(..., description= "Upload your files"), db: Session = Depends(database.get_db)):
   try:
      for file in files:
         contents = file.file.read()
         obj_oid = hash(contents) #! Change this to a better hash function maybe
         new_object = models.Object(name=file.filename, blob=contents, oid= obj_oid)
         db.add(new_object)
      db.commit()

   except Exception as e:
      db.rollback
      return {"message": "There was an error uploading the file(s): {e}"}
   finally:
      db.close()

   return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}    

