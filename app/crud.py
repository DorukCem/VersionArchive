from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

# Warning: does not commit
def get_or_create(session, model, **kwargs):
   instance = session.query(model).filter_by(**kwargs).first()
   if instance:
      return instance
   else:
      instance = model(**kwargs)
      session.add(instance)
   
   return instance

def create_or_error(session, model, **kwargs):
   try:
      instance = model(**kwargs)
      session.add(instance)
      session.commit()
      return instance
   except IntegrityError:
      session.rollback()
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Non-unique entry")
   
def get_one(session, model, **kwargs):
   return session.query(model).filter_by(**kwargs).first()