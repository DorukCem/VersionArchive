from fastapi import FastAPI
from .database import engine
from . import models
from .routers import repository, objects, commits, branch

# * We are currently ignoring folders and only taking in files

# TODO proper routing
# TODO improve api endpoints
# TODO allow branching from previous commits
# TODO allow reset branch to previous commit

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(objects.router)
app.include_router(repository.router)
app.include_router(commits.router)
app.include_router(branch.router)

@app.get("/")
def index():
   return {"Hello World"}
