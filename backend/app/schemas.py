from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
   username: str
   password : str

class Token(BaseModel):
   access_token: str
   token_type: str

class TokenData(BaseModel):
   username: Optional[str] = None

class ObjectResponseSchema(BaseModel):
   id: int
   oid: str
   name: str
   blob: bytes
   repository_id: int

class CommitResponseSchema(BaseModel):
   id: int
   oid: str
   commit_message: str
   parent_oid: Optional[str] = None
   objects: List[ObjectResponseSchema] = []


class BranchResponseSchema(BaseModel):
   id: int
   name: str
   head_commit_oid: Optional[str] = None
   repository_id: int

class ChangeBranchResponse(BaseModel):
   repository_name: str
   branch_name: str

class RepositoryResponseSchema(BaseModel):
   id: int
   name: str
   creator_id: int
   objects: List[ObjectResponseSchema] = []
   commits: List[CommitResponseSchema] = []
   branches: List[BranchResponseSchema] = []

class UserResponseSchema(BaseModel):
   id: int
   name: str
   repositories: List[RepositoryResponseSchema] = []