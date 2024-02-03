from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BLOB, BigInteger
from sqlalchemy.orm import relationship

class Object(Base):
   __tablename__ = "objects"
   oid = Column(String, primary_key= True)
   name = Column(String)
   blob = Column(BLOB)

class Commit(Base):
   __tablename__ = "commits"
   oid = Column(String, primary_key= True)
   commit_message = Column(String)
   parent_oid = Column(String, nullable= True)

   objects = relationship("Object", secondary="commit_object_association")

   repository_id = Column(Integer, ForeignKey("repositories.id"))
   repository = relationship("Repository", back_populates="commits")

class CommitObjectAssociation(Base):
   __tablename__ = 'commit_object_association'
   commit_oid = Column(String, ForeignKey('commits.oid'), primary_key=True)
   object_oid = Column(String, ForeignKey('objects.oid'), primary_key=True)

# TODO lets just look at the files of the previous commit instead
class TrackedObjects(Base):
   __tablename__ = "tracked_objects"
   filename = Column(String, primary_key=True)

class Repository(Base):
   __tablename__ = "repositories"
   id = Column(Integer, primary_key=True, autoincrement= True)
   name = Column(String, unique= True)
   head_oid = Column(String, nullable= True, default= None)

   commits = relationship("Commit", back_populates="repository")