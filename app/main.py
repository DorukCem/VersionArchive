from fastapi import FastAPI
from .database import engine
from . import models
from .routers import repository, objects, commits

# * We are currently ignoring folders and only taking in files
# TODO log commits
# TODO branch
# TODO move head

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(objects.router)
app.include_router(repository.router)
app.include_router(commits.router)

@app.get("/")
def index():
   return {"Hello World"}
