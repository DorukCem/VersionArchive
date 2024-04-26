from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud, utils, schemas
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/object/{user_name}/{repository_name}", tags=["object"])

@router.get("/{branch_name}/all", response_model= List[schemas.ObjectResponseSchema], status_code= status.HTTP_200_OK)
def get_all_for_repository(user_name: str, repository_name : str, branch_name:str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repository = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)
   branch = crud.get_one_or_error(db, models.Branch, name= branch_name, repository_id = repository.id  )
   head_commit = crud.get_one_or_none(db, models.Commit, oid= branch.head_commit_oid, repository_id= repository.id)
   if head_commit:
      return head_commit.objects
   else:
      return []

@router.get("/diff", status_code= status.HTTP_200_OK)
def get_diff_of_objects(obj_oid_1: str, obj_oid_2: str, db: Session = Depends(database.get_db)):
   obj1 = crud.get_one_or_error(db, models.Object, oid= obj_oid_1)
   obj2 = crud.get_one_or_error(db, models.Object, oid= obj_oid_2)

   diff = utils.diff_blobs(obj1.blob, obj2.blob)

   return {"diff": diff}

@router.get("/{object_oid}", response_model=schemas.ObjectResponseSchema,  status_code=status.HTTP_200_OK)
def get_object(user_name:str, repository_name: str, object_oid : str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repository = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)
   object= crud.get_one_or_error(db, models.Object, oid = object_oid, repository_id= repository.id)

   return object
   # The returned content has special chars such as \n and \r
