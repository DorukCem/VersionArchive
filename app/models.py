from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BLOB, Enum, UniqueConstraint
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

class Branch(Base):
   __tablename__ = "branches"
   id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(String)
   
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
   head_oid = Column(String, nullable= True, default= None)
   
   current_branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)
   current_branch = relationship("Branch", uselist=False, foreign_keys=[current_branch_id])

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
   password = Column(String)

   repositories = relationship("Repository", back_populates="creator")