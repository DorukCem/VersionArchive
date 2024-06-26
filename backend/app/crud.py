from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

# Warning: does not commit
def create_or_get(session, model, **kwargs):
   instance = session.query(model).filter_by(**kwargs).first()
   if instance:
      return instance
   else:
      instance = model(**kwargs)
      session.add(instance)
   
   return instance

def create_unique_or_error(session, model, **kwargs):
   try:
      instance = model(**kwargs)
      session.add(instance)
      session.commit()
      return instance
   except IntegrityError:
      session.rollback()
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Non-unique entry")
   
def get_one_or_none(session, model, **kwargs):
   return session.query(model).filter_by(**kwargs).first()

def get_one_or_error(session, model, **kwargs):
   try:
      instance = session.query(model).filter_by(**kwargs).one()
      return instance
   except:
      filters = ", ".join(f"{key}={value}" for key, value in kwargs.items())
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find {model.__name__} with {filters}")

def get_many(session, model, order=None, skip= 0, limit= 100, **kwargs):
   query = session.query(model).filter_by(**kwargs)
   if order:
      query = query.order_by(order)
   return query.offset(skip).limit(limit).all()

def delete(session, db_object):
   session.delete(db_object)
   session.commit()
   return db_object