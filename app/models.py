from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BLOB
from sqlalchemy.orm import relationship

class Object(Base):
   __tablename__ = "objects"
   oid = Column(Integer, primary_key=True)
   name = Column(String)
   blob = Column(BLOB)