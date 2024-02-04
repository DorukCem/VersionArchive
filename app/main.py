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

def merge_old_and_new_objects(old_objects : List[models.Object], new_objects : List[models.Object]):
   """
      Merge old objects and new objects by object.name
      if a file with the same name is in both lists, take the newer one
   """
   name_to_object = {obj.name : obj for obj in old_objects}
   for obj in new_objects:
      name_to_object[obj.name] = obj

   return list(name_to_object.values())


@app.get("/")
def index():
   return {"Hello World"}

@app.post("/upload", status_code=status.HTTP_201_CREATED)
def upload(files: List[UploadFile] = File(..., description= "Upload your files"),
           commit_message: str = Form(..., description="Commit message"),
           db: Session = Depends(database.get_db)):
   try: 
      new_objects = []
      for file in files:
         contents = file.file.read()
         if not contents: # ? We can skip empty files 
            continue

         obj_oid = create_object_oid(contents)
         object = get_or_create(db, models.Object, name=file.filename, blob=contents, oid= str(obj_oid))
         new_objects.append(object)
      
      repository = db.query(models.Repository).filter_by(id=1).first()
      head_oid = repository.head_oid if repository else None
      old_objects =  db.query(models.Commit).filter_by(oid=head_oid).first().objects if head_oid else []
      
      merged_objects = merge_old_and_new_objects(old_objects, new_objects)

      commit_oid = create_commit_oid(merged_objects)
      # ! Hard coded repo_id
      commit = get_or_create(db, models.Commit, oid = commit_oid, 
                    commit_message=commit_message, parent_oid = head_oid, repository_id = 1)
      for obj in merged_objects:
         commit.objects.append(obj)
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

# TODO error checking
@app.get("/working_directory")
def get_working_directory(repo_id : int, db: Session = Depends(database.get_db)):
   repo_head = db.query(models.Repository).filter_by(id= repo_id).first().head_oid
   head_commit = db.query(models.Commit).filter_by(oid= repo_head).first() if repo_head else []
   return [obj.oid for obj in head_commit.objects]
   

@app.post("/create_repo", status_code=status.HTTP_201_CREATED)
def create_repo(repo_name : str, db: Session = Depends(database.get_db)):
   try:
      create_or_error(db, models.Repository, name= repo_name)
      return {"message" : f"succesfully created repository: {repo_name}"}
   except Exception as e:
      raise e