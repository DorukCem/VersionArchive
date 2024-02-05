from fastapi import FastAPI,  Depends
from typing import List
from .database import engine
from sqlalchemy.orm import Session
from . import models, database
from .routers import repository, objects, commits

# * We are currently ignoring folders and only taking in files

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(objects.router)
app.include_router(repository.router)
app.include_router(commits.router)


@app.get("/")
def index():
   return {"Hello World"}

# TODO error checking
@app.get("/working_directory")
def get_working_directory(repo_id : int, db: Session = Depends(database.get_db)):
   repo_head = db.query(models.Repository).filter_by(id= repo_id).first().head_oid
   head_commit = db.query(models.Commit).filter_by(oid= repo_head).first() if repo_head else []
   return [obj.oid for obj in head_commit.objects]
   