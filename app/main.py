from fastapi import FastAPI
from .database import engine
from . import models
from .routers import repository, objects, commits, branch, authentication, users

# * We are currently ignoring folders and only taking in files

# TODO users should only be allowed to work on things that they own
# TODO docs

# * Features will not be added until things above are done
# TODO allow branching from previous commits

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(repository.router)
app.include_router(branch.router)
app.include_router(commits.router)
app.include_router(objects.router)

@app.get("/")
def index():
   return {"Hello World"}
