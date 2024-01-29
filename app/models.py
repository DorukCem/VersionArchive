from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BLOB, BigInteger
from sqlalchemy.orm import relationship

class Object(Base):
   __tablename__ = "objects"
   oid = Column(String, primary_key=True)
   name = Column(String)
   blob = Column(BLOB)