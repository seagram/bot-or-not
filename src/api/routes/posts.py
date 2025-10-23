from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Session, select
from src.models.models import User, Post
from src.database import engine
from src.auth import verify_api_key

class PostCreate(BaseModel):
    author_id: str
    text: str
    created_at: datetime

class PostGet(BaseModel):
    id: str
    author_id: str
    text: str
    created_at: datetime
    lang: str

router = APIRouter(prefix="/post", tags=["posts"])

@router.get("/", response_model=PostGet)
async def get_post(
    id: str,
    api_key: str = Depends(verify_api_key)
):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == id)).first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return PostGet(
            id=post.id,
            author_id=post.author_id,
            text=post.text,
            created_at=post.created_at,
            lang=post.lang
        )

@router.post("/")
async def create_post(
    post_data: PostCreate,
    api_key: str = Depends(verify_api_key)
):
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