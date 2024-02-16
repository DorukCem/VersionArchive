from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud, oauth2, schemas
from sqlalchemy.orm import Session
from typing import List, Optional
import networkx as nx
from networkx.readwrite import json_graph

router = APIRouter(prefix= "/{user_name}", tags=["repository"], dependencies= [Depends(oauth2.get_current_user)])

@router.post("/", response_model= schemas.RepositoryResponseSchema ,status_code=status.HTTP_201_CREATED)
def create_repo(user_name: str, repo_name : str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name)
   repo = crud.create_unique_or_error(db, models.Repository, name= repo_name, creator= user)
   master_branch = crud.create_unique_or_error(db, models.Branch, name= "master", head_commit_oid = None, repository_id= repo.id)

   repo.branches.append(master_branch)
   repo.current_branch_id = master_branch.id
   db.commit()
   return repo

@router.put("/{repository_name}/change-branch", response_model=schemas.ChangeBranchResponse, status_code=status.HTTP_200_OK)
def change_branch(user_name: str, repository_name: str, branch_name: str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name)
   repo = crud.get_one_or_error(db, models.Repository, name= repository_name, creator= user) 
   branch = crud.get_one_or_error(db, models.Branch, name= branch_name, repository_id= repo.id)
   repo.current_branch = branch
   db.commit()
   return schemas.ChangeBranchResponse(repo.name, branch_name=branch.name)

@router.get("/{repository_name}/tree", status_code=status.HTTP_200_OK)
def get_tree_for_repo(user_name: str, repository_name: str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name)
   repo = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id) 
   
   # Create an empty directed graph
   graph = nx.DiGraph()

   for branch in repo.branches:
      head = branch.head_commit_oid
      commit = crud.get_one_or_error(db, models.Commit, oid=head, repository_id= repo.id)
      while commit:
         graph.add_node(commit.oid, label=f"Commit: {commit.commit_message}")

         if commit.parent_oid:
            graph.add_edge(commit.parent_oid, commit.oid)
         else:
            root = commit.oid # Returnning this could be good for drawing better graphs

         commit = crud.get_one_or_none(db, models.Commit, oid=commit.parent_oid, repository_id= repo.id)


   return json_graph.node_link_data(graph)