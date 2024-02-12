from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
   username: str
   password : str

class Token(BaseModel):
   access_token: str
   token_type: str


class TokenData(BaseModel):
   name: Optional[str] = None