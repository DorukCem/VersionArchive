from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/object", tags=["object"])

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
@router.get("/all/{repo_id}")
def get_all_for_repository(repo_id : int, db: Session = Depends(database.get_db)):
   repo_head = db.query(models.Repository).filter_by(id= repo_id).first().head_oid
   head_commit = db.query(models.Commit).filter_by(oid= repo_head).first() if repo_head else []
   return [obj.oid for obj in head_commit.objects]