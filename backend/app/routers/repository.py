from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud, oauth2, schemas
from sqlalchemy.orm import Session
from typing import List, Optional
import networkx as nx
from networkx.readwrite import json_graph

router = APIRouter(prefix= "/repo/{user_name}", tags=["repository"])

@router.post("/create/{repository_name}", response_model= schemas.RepositoryResponseSchema, status_code=status.HTTP_201_CREATED)
def create_repo(repository_name : str, user_name: str, 
                db: Session = Depends(database.get_db)):
   
   user = crud.get_one_or_error(db, models.User, name= user_name)
   repo = crud.create_unique_or_error(db, models.Repository, name= repository_name, creator= user)
   master_branch = crud.create_unique_or_error(db, models.Branch, name= "master", head_commit_id = None, repository_id= repo.id)

   repo.branches.append(master_branch)
   db.commit()
   return repo


@router.get("/{repository_name}/tree", status_code=status.HTTP_200_OK)
def get_tree_for_repo(user_name: str, repository_name: str, depth= 100, db: Session = Depends(database.get_db)):
   """Return the graph formed by commits and branches
       o  → o  →  o  →  o  →  o → o
            ↓                     ↑
            o ← dev_branch    master_branch 
   """
   user = crud.get_one_or_error(db, models.User, name= user_name)
   repo = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id)  
   # Create an empty directed graph
   graph = nx.DiGraph()

   commits_in_repo = crud.get_many(db, models.Commit, limit=depth, repository_id= repo.id)

   for commit in commits_in_repo:
      graph.add_node(commit.oid, label=f"Commit: {commit.commit_message}")
      if commit.parent_oid:
         graph.add_edge(commit.parent_oid, commit.oid)
      else:
         root = commit.oid  # Store the root commit OID for better graph visualization

   return json_graph.node_link_data(graph)

@router.get("/all-repos", response_model=List[str], status_code=status.HTTP_200_OK)
def get_user_repositories(user_name: str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name)
   repositories = crud.get_many(db, models.Repository, creator_id=user.id)
   return [repo.name for repo in repositories]

@router.get("/{repository_name}/all-branches", response_model=List[str], status_code=status.HTTP_200_OK)
def get_repo_branches(user_name: str, repository_name:str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name)
   repo = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id) 
   branches = crud.get_many(db, models.Branch, repository_id = repo.id) 
   return [br.name for br in branches]

@router.get("/{repository_name}", response_model=schemas.RepositoryResponseSchema, status_code=status.HTTP_200_OK)
def get_repo(user_name: str, repository_name:str, db: Session = Depends(database.get_db)):
   user = crud.get_one_or_error(db, models.User, name= user_name)
   repo = crud.get_one_or_error(db, models.Repository, name= repository_name, creator_id= user.id) 
   return repo