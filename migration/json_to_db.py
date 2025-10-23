import msgspec
from datetime import datetime
from typing import List, Optional
from pprint import pprint

'''
msgspec classes for converting JSON to dataclasses
'''

class MetadataTopic(msgspec.Struct):
    topic: str
    keywords: List[str]

class Metadata(msgspec.Struct):
    total_amount_users: int
    total_amount_post: int
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

class ResultUser(msgspec.Struct):
    is_bot: bool
    bot_team_id: int
    bot_team_name: str
    user_id: str

class Detector(msgspec.Struct):
    teamName: str
    isBot: bool
    confidence: int

class ResultDataset(msgspec.Struct):
    id: int
    posts: List[Post]
    user_id: str
    tweet_count: int
    z_score: float
    username: str
    name: str
    description: str
    location: Optional[str]
    detectors: List[Detector]

def main():
    with open("../data/detector_dataset_1.json", "r") as f:
        data = msgspec.json.decode(f.read())
    pprint(data)

    with open("../data/results_dataset_1.json", "r") as f:
        data = msgspec.json.decode(f.read())
    pprint(data)

if __name__ == "__main__":
    main()