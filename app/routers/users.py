from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, crud

from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
   tags= ['user']
)

@router.post("/create-user")
def create_user(request : schemas.User, db: Session = Depends(database.get_db)):
   new_user = crud.create_unique_or_error(db, models.User, name= request.username, password= request.password)
   return new_user