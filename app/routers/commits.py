from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from .. import database, models, crud, utils
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/commit", tags= ["commit"])

@router.post("/{repository_name}", status_code=status.HTTP_201_CREATED)
def commit_files(repository_name: str,
                 files: List[UploadFile] = File(..., description= "Upload your files"),
                 commit_message: str = Form(..., description="Commit message"),
                 db: Session = Depends(database.get_db)):
   try: 
      repository = crud.get_one(db, models.Repository, name= repository_name)
      if not repository:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")
      
      # Put files into db
      new_objects = []
      for file in files:
         contents = file.file.read()
         if not contents: # ? We can skip empty files 
            continue

         obj_oid = utils.create_object_oid(contents)
         object = crud.get_or_create(db, models.Object, name=file.filename, blob=contents, oid= str(obj_oid))
         new_objects.append(object)
      
      # Create new commit object
      head_oid = repository.head_oid if repository else None
      old_objects =  db.query(models.Commit).filter_by(oid=head_oid).first().objects if head_oid else []
      merged_objects = utils.merge_old_and_new_objects(old_objects, new_objects)
      commit_oid = utils.create_commit_oid(merged_objects)
      
      commit = crud.get_or_create(db, models.Commit, oid = commit_oid, 
                    commit_message=commit_message, parent_oid = head_oid, repository_id = repository.id) # ? I handled parent commits in wierd way where they get updated if current branch
    
      for obj in merged_objects:
         commit.objects.append(obj)
      
      # Move branch and head
      repository.head_oid = commit.oid
      if repository.current_branch:
         branch= repository.current_branch
         commit.parent_oid = branch.head_commit_oid
         branch.head_commit_oid = commit.oid

      db.commit()

   except HTTPException as http_exception:
      raise http_exception
   except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
   finally:
      db.close()

   return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

@router.get("/{commit_oid}/objects", status_code=status.HTTP_200_OK)
def get_all_objects_for_commit(commit_oid : str, db: Session = Depends(database.get_db)):
   commit = crud.get_one(db, models.Commit, oid= commit_oid)
   return [obj.oid for obj in commit.objects]

@router.get("/{repository_name}/{branch_name}/log")
def log_commits_in_branch( repository_name : str, branch_name: str, log_depth : int = 10, db: Session = Depends(database.get_db)):
   repo = crud.get_one(db, models.Repository, name= repository_name)
   branch = crud.get_one(db, models.Branch, repository_id= repo.id, name= branch_name)
   head = branch.head_commit_oid
   commit = crud.get_one(db, models.Commit, oid= head)
   commits = []

   while (commit and log_depth):
      commits.append(commit.oid)
      parent_oid = commit.parent_oid
      commit = crud.get_one(db, models.Commit, oid= parent_oid)
      log_depth -= 1

   return commits