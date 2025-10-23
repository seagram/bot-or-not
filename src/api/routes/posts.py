from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Session, select
from models import User, Post
from database import engine

class PostCreate(BaseModel):
    author_id: str
    text: str
    created_at: datetime

router = APIRouter(prefix="/post", tags=["posts"])

@router.get("/")
async def get_post(id: str):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == id)).first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return post

@router.post("/")
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
