from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime

'''
sqlmodel (type-safe orm) classes for defining sqlite tables 
'''

'''
link tables for many-to-many relationships
sqlmodel uses 'relationships' as an abstraction over standard sql normalization
'''

class DatasetPostLink(SQLModel, table=True):
    __tablename__ = "dataset_post_link"
    dataset_id: int = Field(foreign_key="detector_dataset.id", primary_key=True)
    post_id: str = Field(foreign_key="post.id", primary_key=True)

class ResultDatasetPostLink(SQLModel, table=True):
    __tablename__ = "result_dataset_post_link"
    result_dataset_id: int = Field(foreign_key="result_dataset.id", primary_key=True)
    post_id: str = Field(foreign_key="post.id", primary_key=True)

class ResultDatasetUserLink(SQLModel, table=True):
    __tablename__ = "result_dataset_user_link"
    result_dataset_id: int = Field(foreign_key="result_dataset.id", primary_key=True)
    user_id: str = Field(foreign_key="user.id", primary_key=True)

'''
supplemental tables for relationships
'''

class Keyword(SQLModel, table=True):
    __tablename__ = "keyword"
    id: int | None = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="metadata_topic.id", index=True)
    keyword: str
    topic: Optional["MetadataTopic"] = Relationship(back_populates="keywords")

class MetadataTopic(SQLModel, table=True):
    __tablename__ = "metadata_topic"
    id: int | None = Field(default=None, primary_key=True)
    dataset_id: int = Field(foreign_key="detector_dataset.id", index=True)
    topic: str
    keywords: List["Keyword"] = Relationship(back_populates="topic")
    dataset: Optional["DetectorDataset"] = Relationship(back_populates="topics")

class Detector(SQLModel, table=True):
    __tablename__ = "detector"
    id: int | None = Field(default=None, primary_key=True)
    analysis_id: int = Field(foreign_key="user_result.id", index=True)
    team_name: str
    is_bot: bool
    confidence: int = Field(ge=0, le=100)
    analysis: Optional["UserResult"] = Relationship(back_populates="detectors")

'''
main tables
'''

class Post(SQLModel, table=True):
    __tablename__ = "post"
    # client-supplied fields
    author_id: str = Field(foreign_key="user.id", index=True)
    text: str
    created_at: datetime = Field(index=True)
    # server-generated fields
    id: str | None = Field(default=None, primary_key=True)
    lang: str
    author: Optional["User"] = Relationship(back_populates="posts")

class User(SQLModel, table=True):
    __tablename__ = "user"
    # client-supplied fields
    username: str
    name: str
    description: str
    location: Optional[str]
    # server-generated fields
    id: str | None = Field(default=None, primary_key=True)
    tweet_count: int | None 
    z_score: float | None 
    posts: List["Post"] = Relationship(back_populates="author") | None
    users: List["UserResult"] = Relationship(back_populates="user") | None

class UserResult(SQLModel, table=True):
    __tablename__ = "user_result"
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    is_bot: bool
    bot_team_id: int | None
    bot_team_name: str | None
    user: Optional["User"] = Relationship(back_populates="users")
    detectors: List["Detector"] = Relationship(back_populates="analysis")

class DetectorDataset(SQLModel, table=True):
    __tablename__ = "detector_dataset"
    id: int = Field(primary_key=True)
    lang: str
    topics: List["MetadataTopic"] = Relationship(back_populates="dataset")
    posts: List["Post"] = Relationship(link_model=DatasetPostLink)

class ResultDataset(SQLModel, table=True):
    __tablename__ = "result_dataset"
    id: int = Field(primary_key=True)
    posts: List["Post"] = Relationship(link_model=ResultDatasetPostLink)
    users: List["User"] = Relationship(link_model=ResultDatasetUserLink)