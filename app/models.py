from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BLOB, BigInteger
from sqlalchemy.orm import relationship

class Object(Base):
   __tablename__ = "objects"
   oid = Column(String, primary_key= True)
   name = Column(String)
   blob = Column(BLOB)

# ! Currently commits do not need to change anything
class Commit(Base):
   __tablename__ = "commits"
   id = Column(Integer, primary_key= True, autoincrement= True)
   commit_message = Column(String)
   parent_oid = Column(String, nullable= True)

   objects = relationship("Object", secondary="commit_object_association")

class CommitObjectAssociation(Base):
   __tablename__ = 'commit_object_association'
   commit_id = Column(String, ForeignKey('commits.id'), primary_key=True)
   object_oid = Column(String, ForeignKey('objects.oid'), primary_key=True)

class TrackedObjects(Base):
   __tablename__ = "tracked_objects"
   filename = Column(String, primary_key=True)