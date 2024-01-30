from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from typing import List
from .database import engine
from sqlalchemy.orm import Session
from . import models, database
import hashlib

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get("/")
def index():
   return {"Hello World"}

@app.post("/upload", status_code=status.HTTP_201_CREATED)
def upload(files: List[UploadFile] = File(..., description= "Upload your files"), db: Session = Depends(database.get_db)):
   """
      Uploads all given files. Skips files that are already in the db. 
   """
   try:
      commit_message = "Hardcoded commit message"
      commit_oid = "hardcode 123"
      new_commit = models.Commit(commit_message=commit_message, oid = commit_oid, parent = None)

      for file in files:
         contents = file.file.read()
         # ! Check if contents are null
         obj_oid = hashlib.sha1(contents).hexdigest()

         existing_object = db.query(models.Object).filter_by(oid=obj_oid).first()
         if existing_object:
            continue

         new_object = models.Object(name=file.filename, blob=contents, oid= str(obj_oid) )
         new_commit.objects.append(new_object)
         db.add(new_object)
      
      db.add(new_commit)
      db.commit()

   except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
   finally:
      db.close()

   return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

@app.get("/read_file")
def read_file(obj_oid : str, db: Session = Depends(database.get_db)):
   """ Returns the contents of a file """
   object = db.query(models.Object).filter_by(oid = obj_oid).first()
   if not object:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
   
   contents = object.blob.decode("utf-8")
   
   return {"content": contents}
   # The returned content has special chars such as \n and \r

# TODO some sort of error message on commits