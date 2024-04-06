from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud, utils, schemas
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/{user_name}/{repository_name}/object", tags=["object"])

@router.get("/{object_oid}", response_model=schemas.ObjectResponseSchema,  status_code=status.HTTP_200_OK)
def get_object(user_name:str, repository_name: str, object_oid : str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repository = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)
   object= crud.get_one_or_error(db, models.Object, oid = object_oid, repository_id= repository.id)

   return object
   # The returned content has special chars such as \n and \r

@router.get("/all", response_model=List[schemas.ObjectResponseSchema], status_code= status.HTTP_200_OK)
def get_all_for_repository(user_name: str, repository_name : str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repository = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)
   head_commit = crud.get_one_or_error(db, models.Commit, oid= repository.head_oid, repository_id= repository.id)
   return head_commit.objects

@router.get("/diff/", status_code= status.HTTP_200_OK)
def get_diff_of_objects(obj_oid_1: str, obj_oid_2: str, db: Session = Depends(database.get_db)):
   obj1 = crud.get_one_or_error(db, models.Object, oid= obj_oid_1)
   obj2 = crud.get_one_or_error(db, models.Object, oid= obj_oid_2)

   diff = utils.diff_blobs(obj1.blob, obj2.blob)

   return {"diff": diff}