from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/{repository_id}", tags=["branch"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_branch(repository_id : int, branch_name: str, db: Session = Depends(database.get_db)):
   try:
      repo = crud.get_one(db, models.Repository, id = repository_id)
      branch = crud.create_or_error(db, models.Branch, name= branch_name, 
                                    repository_id= repository_id, head_commit_oid= repo.head_oid)
      db.commit()
      return {"message" : f"succesfully created branch: {branch.name} in repository: {repo.name}"}
   
   except Exception as e:
      raise e
   
@router.put("/{branch_name}/reset/{commit_oid}")
def reset_branch_to_previous_commit(repository_id : int, branch_name: str, 
                                    commit_oid: str, db: Session = Depends(database.get_db)):
   repo = crud.get_one(db, models.Repository, id = repository_id)
   commit = crud.get_one(db, models.Commit, oid= commit_oid)
   branch = crud.get_one(db, models.Branch, repository_id = repo.id, name= branch_name)
   if repo.current_branch_id == branch.id:
      repo.head_oid = commit.oid 
   branch.head_oid = commit.oid

   return {"message" : f"succesfully reseted branch {branch.name} to commit {commit.oid}"}