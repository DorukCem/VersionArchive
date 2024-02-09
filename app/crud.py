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

def get_many(session, model, skip= 0, limit= 100, **kwargs):
   return session.query(model).filter_by(**kwargs).offset(skip).limit(limit).all()

def delete(session, db_object):
   session.delete(db_object)
   session.commit()
   return db_object