from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Form
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
def upload(files: List[UploadFile] = File(..., description= "Upload your files"),
           commit_message: str = Form(..., description="Commit message"),
           db: Session = Depends(database.get_db)):
   try: 
      new_commit = models.Commit(commit_message=commit_message, parent_oid = None)

      for file in files:
         contents = file.file.read()
         
         tracked_file_name = db.query(models.TrackedObjects).filter_by(filename=file.filename).first()
         if not tracked_file_name:
            tracked_file_name = models.TrackedObjects(filename=file.filename)
            db.add(tracked_file_name)
         
         if not contents: # ? We can skip empty files 
            continue
         obj_oid = hashlib.sha1(contents).hexdigest()

         object = db.query(models.Object).filter_by(oid=obj_oid).first()
         if object == None:
            object = models.Object(name=file.filename, blob=contents, oid= str(obj_oid) )

         new_commit.objects.append(object)
         db.add(object)
      
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