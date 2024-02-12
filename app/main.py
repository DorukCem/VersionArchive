from fastapi import FastAPI
from .database import engine
from . import models
from .routers import repository, objects, commits, branch, authentication, users

# * We are currently ignoring folders and only taking in files

# TODO proper routing
# TODO improve api endpoints
# TODO allow branching from previous commits
# TODO allow reset branch to previous commit
# TODO users should only be allowed to work on things that they own

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(objects.router)
app.include_router(repository.router)
app.include_router(commits.router)
app.include_router(branch.router)
app.include_router(authentication.router)
app.include_router(users.router)

@app.get("/")
def index():
   return {"Hello World"}
