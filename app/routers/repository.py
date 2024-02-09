from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/repository", tags=["repository"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_repo(repo_name : str, db: Session = Depends(database.get_db)):
   try:
      repo = crud.create_or_error(db, models.Repository, name= repo_name)
      #! hardcoded head_commit
      master_branch = crud.create_or_error(db, models.Branch, name= "master", head_commit_oid = 0, repository_id= repo.id)
      repo.branches.append(master_branch)
      repo.current_branch_id = master_branch.id
      db.commit()
      return {"message" : f"succesfully created repository: {repo_name}"}
   except Exception as e:
      raise e