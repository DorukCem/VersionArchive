from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BLOB, BigInteger
from sqlalchemy.orm import relationship

class Object(Base):
   __tablename__ = "objects"
   oid = Column(String, primary_key= True)
   name = Column(String)
   blob = Column(BLOB)

   commits = relationship("Commit", secondary="commit_object_association")

class Commit(Base):
   __tablename__ = "commits"
   oid = Column(String, primary_key= True)
   commit_message = Column(String)
   parent = Column(String, nullable= True)

   objects = relationship("Object", secondary="commit_object_association")

class CommitObjectAssociation(Base):
   __tablename__ = 'commit_object_association'
   commit_oid = Column(String, ForeignKey('commits.oid'), primary_key=True)
   object_oid = Column(String, ForeignKey('objects.oid'), primary_key=True)
