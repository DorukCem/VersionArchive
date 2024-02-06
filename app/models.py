from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BLOB, Enum
from sqlalchemy.orm import relationship
import enum

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

class Branch(Base):
   __tablename__ = "branches"
   id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(String, unique=True)
   
   head_commit_oid = Column(String, ForeignKey("commits.oid"))
   repository_id = Column(Integer, ForeignKey("repositories.id"))
   repository = relationship("Repository", back_populates="branches")

class HeadRef(enum.Enum):
   branch = 0
   commit = 1

class Repository(Base):
   __tablename__ = "repositories"
   id = Column(Integer, primary_key=True, autoincrement= True)
   name = Column(String, unique= True)
   head_oid = Column(String, nullable= True, default= None)
   # Indicating if the head is following a branch or a commit
   head_pointing_to = Column(Enum(HeadRef), default= HeadRef.branch)

   commits = relationship("Commit", back_populates="repository")
   branches = relationship("Branch", back_populates="repository")