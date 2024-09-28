from fastapi import FastAPI
from .database import engine
from . import models
from .routers import repository, objects, commits, branch, authentication, users
from fastapi.middleware.cors import CORSMiddleware

# python3 -m uvicorn backend.app.main:app --reload

# * We are currently ignoring folders and only taking in files

# * Features will not be added until things above are done
# TODO allow branching from previous commits
# TODO remove tracked object

app = FastAPI()

models.Base.metadata.create_all(engine)

origins = [
   "http://localhost:5173",
   "localhost:5173"
]

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(repository.router)
app.include_router(branch.router)
app.include_router(commits.router)
app.include_router(objects.router)

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"]
)

@app.get("/")
def index():
   return {"Hello World"}
