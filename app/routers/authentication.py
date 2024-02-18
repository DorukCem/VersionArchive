from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas,database, models, crud, oauth2

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
   tags= ['Authentication']
)

@router.post('/token', response_model= schemas.Token)
def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
   user = oauth2.authenticate_user(db, form_data.username, form_data.password)
   if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
   access_token = oauth2.create_access_token(data={"sub": user.name})
   return {"access_token": access_token, "token_type": "bearer"}