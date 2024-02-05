from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/repository", tags=["repository"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_repo(repo_name : str, db: Session = Depends(database.get_db)):
   try:
      crud.create_or_error(db, models.Repository, name= repo_name)
      return {"message" : f"succesfully created repository: {repo_name}"}
   except Exception as e:
      raise e