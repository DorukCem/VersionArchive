from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from .. import database, models, crud, utils, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/{user_name}/{repository_name}", tags= ["commit"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def commit_files(user_name: str, repository_name: str, 
                 files: List[UploadFile] = File(..., description= "Upload your files"),
                 commit_message: str = Form(..., description="Commit message"),
                 db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
   """
      Commit files to a repository.

      First we create the object models for the files and add them to the database
      Then we create a commit object which points to these objects
      
      We also add any object pointed by the previous commit if they were NOT updated with the new commit 
         This is usually not done in a git system. However we need a way to have something like a working directory
         We are assuming that users still want to track files unless they explictly remove them 

      Lastly we move the branch and repo heads to point at the latets commit
   """
   if current_user.name != user_name:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to commit for another user")
   try:
      user = crud.get_one_or_error(db, models.User, name= user_name) 
      repository = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)
      
      # Put files into db
      new_objects = []
      for file in files:
         contents = file.file.read()
         if not contents: # ? We can skip empty files 
            continue

         obj_oid = utils.create_object_oid(contents)
         object = crud.create_or_get(db, models.Object, name=file.filename, 
                                     blob=contents, oid= str(obj_oid), repository_id = repository.id)
         new_objects.append(object)
      
      # Create new commit object
      head_oid = repository.head_oid
      old_objects =  db.query(models.Commit).filter_by(oid=head_oid).first().objects if head_oid else []
      merged_objects = utils.merge_old_and_new_objects(old_objects, new_objects)
      commit_oid = utils.create_commit_oid(merged_objects)
      commit = crud.create_or_get(db, models.Commit, oid = commit_oid, commit_message=commit_message, 
                                  parent_oid = head_oid, repository_id = repository.id) 
      for obj in merged_objects:
         commit.objects.append(obj)
      
      # Move branch and head
      repository.head_oid = commit.oid
      if repository.current_branch:
         branch= repository.current_branch
         commit.parent_oid = branch.head_commit_oid
         branch.head_commit_oid = commit.oid

      db.commit()

   except Exception as e:
      db.rollback()
      raise e
   finally:
      db.close()

   return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

@router.get("/{commit_oid}/objects", response_model=List[schemas.ObjectResponseSchema], status_code=status.HTTP_200_OK)
def get_all_objects_for_commit(commit_oid : str, repository_name: str, user_name: str, 
                               db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repository = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)
   commit = crud.get_one_or_error(db, models.Commit, oid= commit_oid, repository_id= repository.id)
   return commit.objects
