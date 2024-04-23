from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, crud, oauth2
from typing import Annotated

from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
   tags= ['user']
)

@router.post("/user/create-user")
def create_user(request : schemas.User, db: Session = Depends(database.get_db)): 
   hashed_password= oauth2.get_password_hash(request.password)
   new_user = crud.create_unique_or_error(db, models.User, name= request.username, hashed_password= hashed_password)
   return new_user

@router.get("/user/me")
async def read_users_me(current_user : models.User= Depends(oauth2.get_current_user)):
   return current_user