from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix= "/branch/{user_name}/{repository_name}", tags=["branch"])

@router.post("/new", response_model= schemas.BranchResponseSchema, status_code=status.HTTP_201_CREATED)
def create_branch(user_name: str, repository_name : str, branch_data:schemas.BranchCreateSchema, 
                  db: Session = Depends(database.get_db)):

   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repo = crud.get_one_or_error(db, models.Repository, name = repository_name, creator_id= user.id)
   current_branch = crud.get_one_or_error(db, models.Branch, name = branch_data.old_branch_name, repository_id=repo.id)
   new_branch = crud.create_unique_or_error(db, models.Branch, name= branch_data.new_branch_name, 
                                 repository_id= repo.id, head_commit_id= current_branch.head_commit_id)
   db.commit()
   return new_branch


@router.get("/{branch_name}", response_model= schemas.BranchResponseSchema, status_code=status.HTTP_200_OK)
def get_branch(user_name: str, repository_name : str, branch_name:str, 
                  db: Session = Depends(database.get_db)):

   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repo = crud.get_one_or_error(db, models.Repository, name = repository_name, creator_id= user.id)
   current_branch = crud.get_one_or_error(db, models.Branch, name = branch_name, repository_id=repo.id)
   return current_branch
   
@router.get("/{branch_name}/commits", response_model= List[schemas.CommitOverviewResponseSchema], status_code=status.HTTP_200_OK)
def get_branch_commits(user_name: str, repository_name : str, branch_name:str, 
                  db: Session = Depends(database.get_db)):

   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repo = crud.get_one_or_error(db, models.Repository, name = repository_name, creator_id= user.id)
   current_branch = crud.get_one_or_error(db, models.Branch, name = branch_name, repository_id=repo.id)
   head = current_branch.head_commit_id
   commits_in_repo = crud.get_many(db, models.Commit, repository_id= repo.id)
   commits_in_repo = {c.id: c for c in commits_in_repo}
   commits_in_branch = []
   while(head):
      commit = commits_in_repo[head]
      commits_in_branch.append(commit)
      head = commit.parent_id 
   return commits_in_branch
   
   
@router.put("/{branch_name}/reset/{commit_id}", 
            response_model= schemas.BranchResponseSchema, status_code=status.HTTP_200_OK )
def reset_branch_to_previous_commit(repository_name : str, user_name: str, branch_name: str, 
                                    commit_id: int, db: Session = Depends(database.get_db)):
   """ reset the state of branch to a previous commit by moving the branch head reference
     c1 → c2 → c3 → c4 → c5
                         ↑
                        branch 
   """
   user = crud.get_one_or_error(db, models.User, name= user_name) 
   repo = crud.get_one_or_error(db, models.Repository, name = repository_name, creator_id= user.id)
   commit = crud.get_one_or_error(db, models.Commit, id= commit_id)
   branch = crud.get_one_or_error(db, models.Branch, repository_id = repo.id, name= branch_name)

   branch.head_commit_id = commit.id
   db.commit()
   return branch