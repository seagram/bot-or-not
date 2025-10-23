from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Session, select
from models import User
from database import engine

class UserCreate(BaseModel):
    username: str
    name: str
    description: str
    location: Optional[str] = None

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/")
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

@router.post("/")
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
