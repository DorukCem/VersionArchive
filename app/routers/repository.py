from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, crud
from sqlalchemy.orm import Session
from typing import List, Optional
import networkx as nx
from networkx.readwrite import json_graph

router = APIRouter(prefix= "/repository", tags=["repository"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_repo(repo_name : str, db: Session = Depends(database.get_db)):
   try:
      repo = crud.create_or_error(db, models.Repository, name= repo_name)
      master_branch = crud.create_or_error(db, models.Branch, name= "master", head_commit_oid = None, repository_id= repo.id)
      repo.branches.append(master_branch)
      repo.current_branch_id = master_branch.id
      db.commit()
      return {"message" : f"succesfully created repository: {repo_name}"}
   except Exception as e:
      raise e
   
@router.put("/{repository_name}/change-branch", status_code=status.HTTP_200_OK)
def change_branch(repository_name: str, branch_name: str, db: Session = Depends(database.get_db)):
   repo = crud.get_one(db, models.Repository, name= repository_name) #! This by itself will not be enough when different users are implemented
   branch = crud.get_one(db, models.Branch, name= branch_name)
   repo.current_branch = branch
   db.commit()
   return {"message" : f"succesfully changed branch to {branch_name} in repository {repo.name}"}

@router.get("/{repository_name}/tree", status_code=status.HTTP_200_OK)
def get_tree_for_repo(repository_name: str, db: Session = Depends(database.get_db)):
   repo = crud.get_one(db, models.Repository, name= repository_name) 
   
   # Create an empty directed graph
   graph = nx.DiGraph()

   for branch in repo.branches:
      head = branch.head_commit_oid
      commit = crud.get_one(db, models.Commit, oid=head)
      while commit:
         graph.add_node(commit.oid, label=f"Commit: {commit.commit_message}")

         if commit.parent_oid:
            graph.add_edge(commit.parent_oid, commit.oid)
         else:
            root = commit.oid # Returnning this could be good for drawing better graphs

         commit = crud.get_one(db, models.Commit, oid=commit.parent_oid)


   return json_graph.node_link_data(graph)