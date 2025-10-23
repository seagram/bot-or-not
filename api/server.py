from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from models import User, Post
from sqlmodel import Session, create_engine, select
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(DATABASE_URL, echo=True)

class UserCreate(BaseModel):
    username: str
    name: str
    description: str
    location: Optional[str] = None

class PostCreate(BaseModel):
    author_id: str
    text: str
    created_at: datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "to be or not to be. that is the bot's question."}

'''
user endpoints
'''

@app.get("/user/")
async def get_user(id: Optional[str] = None, username: Optional[str] = None):
    if not id and not username:
        raise HTTPException(status_code=400, detail="Must provide either id or username")

    with Session(engine) as session:
        if id:
            user = session.exec(select(User).where(User.id == id)).first()
        else:
            user = session.exec(select(User).where(User.username == username)).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

@app.post("/user/")
async def create_user(user_data: UserCreate):
    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(User.username == user_data.username)
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        new_user = User(
            username=user_data.username,
            name=user_data.name,
            description=user_data.description,
            location=user_data.location,
            tweet_count=None,
            z_score=None
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user

'''
post endpoints
'''

@app.get("/post/")
async def get_post(id: str):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == id)).first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return post

@app.post("/post/")
async def create_post(post_data: PostCreate):
    with Session(engine) as session:
        author = session.exec(
            select(User).where(User.id == post_data.author_id)
        ).first()

        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        new_post = Post(
            author_id=post_data.author_id,
            text=post_data.text,
            created_at=post_data.created_at,
            lang=""
        )

        session.add(new_post)
        session.commit()
        session.refresh(new_post)

        return new_post

'''
additional endpoints
@app.get("/detector/")
@app.get("/result/")
'''