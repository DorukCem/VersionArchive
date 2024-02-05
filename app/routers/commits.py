from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from .. import database, models, crud, utils
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/commit", tags= ["commit"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def commit_files(files: List[UploadFile] = File(..., description= "Upload your files"),
           commit_message: str = Form(..., description="Commit message"),
           db: Session = Depends(database.get_db)):
   try: 
      new_objects = []
      for file in files:
         contents = file.file.read()
         if not contents: # ? We can skip empty files 
            continue

         obj_oid = utils.create_object_oid(contents)
         object = crud.get_or_create(db, models.Object, name=file.filename, blob=contents, oid= str(obj_oid))
         new_objects.append(object)
      
      repository = db.query(models.Repository).filter_by(id=1).first()
      head_oid = repository.head_oid if repository else None
      old_objects =  db.query(models.Commit).filter_by(oid=head_oid).first().objects if head_oid else []
      
      merged_objects = utils.merge_old_and_new_objects(old_objects, new_objects)

      commit_oid = utils.create_commit_oid(merged_objects)
      # ! Hard coded repo_id
      commit = crud.get_or_create(db, models.Commit, oid = commit_oid, 
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

@router.get("/{commit_oid}/objects", status_code=status.HTTP_200_OK)
def get_all_objects_for_commit(commit_oid : str, db: Session = Depends(database.get_db)):
   pass