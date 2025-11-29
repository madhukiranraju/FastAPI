from fastapi import FastAPI,  Depends
from random import randrange
from sqlalchemy.orm import Session
from . import Model
from .database import engine, get_db
from .routers import Post, User, Auth, Vote
from fastapi.middleware.cors import CORSMiddleware

# Model.Base.metadata.create_all(bind=engine)

app = FastAPI()  

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "www.google.com",#test purpose only
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Post.router)
app.include_router(User.router)
app.include_router(Auth.router)
app.include_router(Vote.router)

@app.get("/")
async def root():
    return {"message": "This is the root endpoint...."}


@app.get("/sqlalchemy")
async def test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(Model.Post).all()
    print(posts)
    return {"data": posts}