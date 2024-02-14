from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud, utils
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/{user_name}/{repository_name}/object", tags=["object"])

@router.get("/{object_oid}",  status_code=status.HTTP_200_OK)
def fetch_object_content(object_oid : str, db: Session = Depends(database.get_db)):
   """ Returns the contents of a file """
   object = db.query(models.Object).filter_by(oid = object_oid).first()
   if not object:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
   
   contents = object.blob.decode("utf-8")
   
   return {"content": contents}
   # The returned content has special chars such as \n and \r

# TODO error checking
@router.get("/all")
def get_all_for_repository(user_name: str, repository_name : str, db: Session = Depends(database.get_db)):
   user = crud.get_one(db, models.User, name= user_name) 
   repo = db.query(models.Repository).filter_by(repository_name= repository_name, creator_id= user.id).first()
   head_commit = db.query(models.Commit).filter_by(oid= repo.head_oid).first() if repo.head_oid else []
   return [obj.oid for obj in head_commit.objects]

@router.get("/diff/")
def get_diff_of_objects(obj_oid_1: str, obj_oid_2: str, db: Session = Depends(database.get_db)):
   obj1 = crud.get_one(db, models.Object, oid= obj_oid_1)
   obj2 = crud.get_one(db, models.Object, oid= obj_oid_2)

   diff = utils.diff_blobs(obj1.blob, obj2.blob)

   return {"diff": diff}