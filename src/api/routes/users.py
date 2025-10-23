from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Session, select
from src.models.models import User
from src.database import engine
from src.auth import verify_api_key

class UserCreate(BaseModel):
    '''
    - defines the required fields a competitior provides to create a user
    - other user fields like id, tweet_count, etc. are generated dynamically server-side
    '''
    username: str
    name: str
    description: str
    location: Optional[str] = None

class UserGet(BaseModel):
    '''
    - defines the attributes returned from getting a user
    '''
    id: str
    username: str
    name: str
    description: str
    location: Optional[str] = None
    tweet_count: int | None = None
    z_score: float | None = None

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/", response_model=UserGet)
async def get_user(
    id: Optional[str] = None,
    username: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
) -> UserGet:
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
async def create_user(
    user_data: UserCreate,
    api_key: str = Depends(verify_api_key)
) -> UserGet:
    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(User.username == user_data.username)
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail=f"User with username {user_data.username} already exists")

        new_user = User(
            username=user_data.username,
            name=user_data.name,
            description=user_data.description,
            location=user_data.location
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
