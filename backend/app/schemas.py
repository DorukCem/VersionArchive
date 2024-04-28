from pydantic import BaseModel
from typing import List, Optional
import datetime

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

class CommitResponseSchema(BaseModel):
   id: int
   oid: str
   commit_message: str
   parent_oid: Optional[str] = None
   objects: List[ObjectResponseSchema] = []

class CommitOverviewResponseSchema(BaseModel):
   id: int
   oid: str
   commit_message: str
   timestamp: datetime.datetime
   parent_oid: Optional[str] = None

class BranchResponseSchema(BaseModel):
   id: int
   name: str
   head_commit_oid: Optional[str] = None
   repository_id: int
   commits: List[CommitOverviewResponseSchema] = []


class BranchCreateSchema(BaseModel):
   old_branch_name: str
   new_branch_name: str

class RepositoryResponseSchema(BaseModel):
   id: int
   name: str
   branches: List[BranchResponseSchema] = []

class UserResponseSchema(BaseModel):
   id: int
   name: str
   repositories: List[RepositoryResponseSchema] = []