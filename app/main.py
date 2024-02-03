from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Form
from typing import List
from .database import engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, database
import hashlib

# * We are currently ignoring folders and only taking in files

app = FastAPI()

models.Base.metadata.create_all(engine)

# Warning: does not commit
def get_or_create(session, model, **kwargs):
   instance = session.query(model).filter_by(**kwargs).first()
   if instance:
      return instance
   else:
      instance = model(**kwargs)
      session.add(instance)
   
   return instance

def create_or_error(session, model, **kwargs):
   try:
      instance = model(**kwargs)
      session.add(instance)
      session.commit()
      return instance
   except IntegrityError:
      session.rollback()
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Non-unique entry")

def create_object_oid(blob):
   return hashlib.sha1(blob).hexdigest()

def create_commit_oid(objects):
   return hashlib.sha1( "".join(sorted([obj.oid for obj in objects])).encode() ).hexdigest()

@app.get("/")
def index():
   return {"Hello World"}

@app.post("/upload", status_code=status.HTTP_201_CREATED)
def upload(files: List[UploadFile] = File(..., description= "Upload your files"),
           commit_message: str = Form(..., description="Commit message"),
           db: Session = Depends(database.get_db)):
   try: 
      objects = []
      for file in files:
         get_or_create(db, models.TrackedObjects, filename= file.filename)

         contents = file.file.read()
         if not contents: # ? We can skip empty files 
            continue

         obj_oid = create_object_oid(contents)
         object = get_or_create(db, models.Object, name=file.filename, blob=contents, oid= str(obj_oid))
         objects.append(object)

      commit_oid = create_commit_oid(objects)
      # ! Hard coded repo_id
      repository = db.query(models.Repository).filter_by(id=1).first()
      head_oid = repository.head_oid if repository else None
      commit = get_or_create(db, models.Commit, oid = commit_oid, 
                    commit_message=commit_message, parent_oid = head_oid, repository_id = 1)
      repository.head_oid = commit.oid

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

@app.post("/create_repo", status_code=status.HTTP_201_CREATED)
def create_repo(repo_name : str, db: Session = Depends(database.get_db)):
   try:
      create_or_error(db, models.Repository, name= repo_name)
      return {"message" : f"succesfully created repository: {repo_name}"}
   except Exception as e:
      raise e