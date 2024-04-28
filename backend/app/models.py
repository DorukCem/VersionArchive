from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BLOB, Enum, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Object(Base):
   """
    Represents an file an its contents in a version control system.

    Attributes:
    - id (int): The unique identifier for the object.
    - oid (str): The SHA-1 hash of the object's contents.
    - name (str): The name of the object.
    - blob (bytes): The binary content of the object (e.g., file contents).
    - repository_id (int): The foreign key reference to the repository to which the object belongs.
    
    - UniqueConstraint: 
      Ensures that each combination of oid and repository_id is unique,
      preventing objects with the same oid from being associated with the same repository more than once.
   """
   __tablename__ = "objects"
   id = Column(Integer, primary_key= True, autoincrement= True)
   oid = Column(String, unique=True, nullable= False) 
   name = Column(String)
   blob = Column(BLOB)

class Commit(Base):
   __tablename__ = "commits"
   id = Column(Integer, primary_key= True, autoincrement= True)
   oid = Column(String, nullable= False)
   commit_message = Column(String)
   timestamp = Column(DateTime(timezone= True), server_default=func.now())
   # Oid of the commit before this commit
   parent_oid = Column(String, nullable= True)

   repository_id = Column(Integer, ForeignKey("repositories.id"), nullable= False)
   repository = relationship("Repository", back_populates="commits")
   objects = relationship("Object", secondary="commit_object_association")

# Many to Many 
class CommitObjectAssociation(Base):
   __tablename__ = 'commit_object_association'
   commit_oid = Column(String, ForeignKey('commits.oid'), primary_key=True)
   object_oid = Column(String, ForeignKey('objects.oid'), primary_key=True)

class Branch(Base):
   __tablename__ = "branches"
   id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(String)
   
   # The last commit that the branch is pointing to
   """ o  → o  →  o  →  o  →  o → o
            ↓                     ↑
            o ← dev_branch    master_branch 
   """
   head_commit_oid = Column(String, ForeignKey("commits.oid"))
   
   repository_id = Column(Integer, ForeignKey("repositories.id"))
   repository = relationship("Repository", back_populates="branches", foreign_keys=[repository_id])

   __table_args__ = (
      UniqueConstraint('name', 'repository_id', name='unique_branch_per_repo'),
   )


class Repository(Base):
   __tablename__ = "repositories"
   id = Column(Integer, primary_key=True, autoincrement= True)
   name = Column(String)

   creator_id = Column(Integer, ForeignKey('users.id'), nullable= False)
   creator = relationship("User", back_populates="repositories")

   commits = relationship("Commit", back_populates="repository")
   branches = relationship("Branch", back_populates="repository", foreign_keys="Branch.repository_id")

   __table_args__ = (
      UniqueConstraint('name', 'creator_id', name='unique_repo_per_user'),
   )

class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, unique= True)
   hashed_password = Column(String)
   disabled = Column(Boolean, default= False)

   repositories = relationship("Repository", back_populates="creator")