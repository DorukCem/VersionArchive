from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud, utils
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/{user_name}/{repository_name}/object", tags=["object"])

@router.get("/{object_oid}",  status_code=status.HTTP_200_OK)
def fetch_object_content(user_name:str, repository_name: str, object_oid : str, db: Session = Depends(database.get_db)):
   """ Returns the contents of a file """
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repository = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)
   object= crud.get_one_or_error(db, models.Object, oid = object_oid, repository_id= repository.id)
   
   contents = object.blob.decode("utf-8")
   
   return {"content": contents}
   # The returned content has special chars such as \n and \r

@router.get("/all")
def get_all_for_repository(user_name: str, repository_name : str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repository = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)
   head_commit = crud.get_one_or_error(db, models.Commit, oid= repository.head_oid, repository_id= repository.id)
   return [obj.oid for obj in head_commit.objects]

@router.get("/diff/")
def get_diff_of_objects(obj_oid_1: str, obj_oid_2: str, db: Session = Depends(database.get_db)):
   obj1 = crud.get_one_or_error(db, models.Object, oid= obj_oid_1)
   obj2 = crud.get_one_or_error(db, models.Object, oid= obj_oid_2)

   diff = utils.diff_blobs(obj1.blob, obj2.blob)

   return {"diff": diff}