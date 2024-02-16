from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/{user_name}/{repository_name}", tags=["branch"])

@router.post("/{branch_name}", status_code=status.HTTP_201_CREATED)
def create_branch(user_name: str, repository_name : str, branch_name: str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repo = crud.get_one_or_error(db, models.Repository, name = repository_name, creator_id= user.id)
   branch = crud.create_unique_or_error(db, models.Branch, name= branch_name, 
                                 repository_id= repo.id, head_commit_oid= repo.head_oid)
   db.commit()
   return {"message" : f"succesfully created branch: {branch.name} in repository: {repo.name}"}
   
   
@router.put("/{branch_name}/reset/{commit_oid}")
def reset_branch_to_previous_commit(repository_name : str, user_name: str, branch_name: str, 
                                    commit_oid: str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repo = crud.get_one_or_error(db, models.Repository, name = repository_name, creator_id= user.id)
   commit = crud.get_one_or_error(db, models.Commit, oid= commit_oid)
   branch = crud.get_one_or_error(db, models.Branch, repository_id = repo.id, name= branch_name)
   if repo.current_branch_id == branch.id:
      repo.head_oid = commit.oid 
   branch.head_oid = commit.oid
   db.commit()
   return {"message" : f"succesfully reseted branch {branch.name} to commit {commit.oid}"}