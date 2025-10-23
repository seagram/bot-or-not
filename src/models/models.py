from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime

class Detector(SQLModel, table=True):
    __tablename__ = "detector"
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    team_name: str
    is_bot: bool
    confidence: int = Field(ge=0, le=100)
    user: Optional["User"] = Relationship(back_populates="detectors")

class Post(SQLModel, table=True):
    __tablename__ = "post"
    author_id: str = Field(foreign_key="user.id", index=True)
    text: str
    created_at: datetime = Field(index=True)
    id: str | None = Field(default=None, primary_key=True)
    lang: str
    author: Optional["User"] = Relationship(back_populates="posts")

class User(SQLModel, table=True):
    __tablename__ = "user"
    id: str | None = Field(default=None, primary_key=True)
    username: str
    name: str
    description: str
    location: Optional[str] = None
    tweet_count: int | None = None
    z_score: float | None = None
    is_bot: bool | None = None
    bot_team_id: int | None = None
    bot_team_name: str | None = None
    posts: List["Post"] = Relationship(back_populates="author")
    detectors: List["Detector"] = Relationship(back_populates="user")