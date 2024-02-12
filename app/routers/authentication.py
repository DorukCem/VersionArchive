from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas,database, models, token, crud

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
   tags= ['Authentication']
)

@router.post('/login')
def login(request : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
   user = crud.get_one(db, models.User, name= request.username, password= request.password)
   if not user:
      raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail= f"Invalid Credentials")
   

   access_token = token.create_access_token( data={"sub": user.name} )
   return {"access_token": access_token, "token_type": "bearer"}