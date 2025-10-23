import msgspec
from datetime import datetime
from typing import List, Optional, Union

'''
msgspec classes for converting JSON to type-safe python classes
'''

'''
clases for detector datasets:
'''

class MetadataTopic(msgspec.Struct):
    topic: str
    keywords: List[str]

class Metadata(msgspec.Struct):
    total_amount_users: int
    total_amount_posts: int
    topics: List[MetadataTopic]
    users_average_amount_posts: float
    users_average_z_score: float

class Post(msgspec.Struct):
    text: str
    created_at: datetime
    id: str
    author_id: str
    lang: str

class User(msgspec.Struct):
    id: str
    tweet_count: int
    z_score: float
    username: str
    name: str
    description: str
    location: Optional[str]

class DetectorDataset(msgspec.Struct):
    id: int
    lang: str
    metadata: Metadata
    posts: List[Post]

'''
classes for result datasets:
'''

class Detector(msgspec.Struct):
    teamName: str
    isBot: bool
    confidence: int

class ResultUser(msgspec.Struct):
    is_bot: bool
    bot_team_id: Union[int, str]
    bot_team_name: str
    user_id: str
    tweet_count: int
    z_score: float
    username: str
    name: str
    description: str
    location: Optional[str]
    detectors: List[Detector]

class ResultDataset(msgspec.Struct):
    id: int
    posts: List[Post]
    users: List[ResultUser]