from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import crud, models, database
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" #! This probably should not be here
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

def verifiy_password(plain_password, hashed_pasword):
   return pwd_context.verify(plain_password, hashed_pasword)

def get_password_hash(password):
   return pwd_context.hash(password)

def authenticate_user(db, username:str, password:str):
   user = crud.get_one_or_none(db, models.User, name= username)
   if not user:
      return False
   if not verifiy_password(password, user.hashed_password):
      return False
   
   return user

def create_access_token(data: dict):
   to_encode = data.copy()
   expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return encoded_jwt

def verify_token(token : str, credentials_exception):
   try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username: str = payload.get("sub")
      if username is None:
         raise credentials_exception
      
      token_data = schemas.TokenData(username=username)
      return token_data
      
   except JWTError:
      raise credentials_exception
   
async def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
   credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
   )
   token_data =  verify_token(token, credentials_exception)
   
   user = crud.get_one_or_none(db, models.User, name= token_data.username)
   if user is None:
      raise credentials_exception
   
   return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
   if current_user.disabled:
      raise HTTPException(status_code=400, detail="Inactive user")
   return current_user