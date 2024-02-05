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