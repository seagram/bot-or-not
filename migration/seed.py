import msgspec
import os
from pathlib import Path
from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
from schemas import DetectorDataset as DetectorDatasetSchema, ResultDataset as ResultDatasetSchema
from models import DetectorDataset, ResultDataset, Post, User, UserResult, MetadataTopic, Keyword, Detector, DatasetPostLink, ResultDatasetPostLink, ResultDatasetUserLink

def load_dataset(file_path: str) -> DetectorDatasetSchema | ResultDatasetSchema:
    filename = Path(file_path).name
    with open(file_path, "r") as f:
        content = f.read()
        if "detector" in filename:
            return msgspec.json.decode(content, type=DetectorDatasetSchema)
        elif "results" in filename:
            return msgspec.json.decode(content, type=ResultDatasetSchema)
        else:
            raise ValueError(f"Unknown dataset type for {filename}")

def convert_detector_dataset_to_models(schema_dataset: DetectorDatasetSchema, session: Session):
    detector_dataset = DetectorDataset(
        id=schema_dataset.id,
        lang=schema_dataset.lang
    )
    session.add(detector_dataset)
    session.flush()

    for topic_schema in schema_dataset.metadata.topics:
        topic = MetadataTopic(
            dataset_id=detector_dataset.id,
            topic=topic_schema.topic
        )
        session.add(topic)
        session.flush()

        for keyword_str in topic_schema.keywords:
            keyword = Keyword(
                topic_id=topic.id,
                keyword=keyword_str
            )
            session.add(keyword)

    user_ids = set()
    for post_schema in schema_dataset.posts:
        if post_schema.author_id not in user_ids:
            user = session.get(User, post_schema.author_id)
            if not user:
                user = User(
                    id=post_schema.author_id,
                    tweet_count=0,
                    z_score=0.0,
                    username="",
                    name="",
                    description=""
                )
                session.add(user)
            user_ids.add(post_schema.author_id)

        post = session.get(Post, post_schema.id)
        if not post:
            post = Post(
                id=post_schema.id,
                author_id=post_schema.author_id,
                text=post_schema.text,
                created_at=post_schema.created_at,
                lang=post_schema.lang
            )
            session.add(post)

        link = DatasetPostLink(
            dataset_id=detector_dataset.id,
            post_id=post_schema.id
        )
        session.add(link)

    session.commit()

def convert_result_dataset_to_models(schema_dataset: ResultDatasetSchema, session: Session):
    result_dataset = ResultDataset(id=schema_dataset.id)
    session.add(result_dataset)
    session.flush()

    for user_schema in schema_dataset.users:
        bot_team_id = int(user_schema.bot_team_id) if isinstance(user_schema.bot_team_id, str) else user_schema.bot_team_id

        user = session.get(User, user_schema.user_id)
        if user:
            user.tweet_count = user_schema.tweet_count
            user.z_score = user_schema.z_score
            user.username = user_schema.username
            user.name = user_schema.name
            user.description = user_schema.description
            user.location = user_schema.location
        else:
            user = User(
                id=user_schema.user_id,
                tweet_count=user_schema.tweet_count,
                z_score=user_schema.z_score,
                username=user_schema.username,
                name=user_schema.name,
                description=user_schema.description,
                location=user_schema.location
            )
            session.add(user)
        session.flush()

        analysis_result = UserResult(
            user_id=user_schema.user_id,
            is_bot=user_schema.is_bot,
            bot_team_id=bot_team_id,
            bot_team_name=user_schema.bot_team_name
        )
        session.add(analysis_result)
        session.flush()

        for detector_schema in user_schema.detectors:
            detector = Detector(
                analysis_id=analysis_result.id,
                team_name=detector_schema.teamName,
                is_bot=detector_schema.isBot,
                confidence=detector_schema.confidence
            )
            session.add(detector)

        link = ResultDatasetUserLink(
            result_dataset_id=result_dataset.id,
            user_id=user_schema.user_id
        )
        session.add(link)

    for post_schema in schema_dataset.posts:
        post = session.get(Post, post_schema.id)
        if not post:
            post = Post(
                id=post_schema.id,
                author_id=post_schema.author_id,
                text=post_schema.text,
                created_at=post_schema.created_at,
                lang=post_schema.lang
            )
            session.add(post)

        link = ResultDatasetPostLink(
            result_dataset_id=result_dataset.id,
            post_id=post_schema.id
        )
        session.add(link)

    session.commit()

def main():
    load_dotenv()
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise ValueError("DB_URL environment variable is not set")
    engine = create_engine(db_url)
    SQLModel.metadata.create_all(engine)
    data_dir = Path(__file__).parent.parent / "data"
    detector_files = sorted(data_dir.glob("*detector*.json"))
    result_files = sorted(data_dir.glob("*results*.json"))

    with Session(engine) as session:
        for detector_file in detector_files:
            detector_dataset_schema = load_dataset(str(detector_file))
            convert_detector_dataset_to_models(detector_dataset_schema, session)

        for result_file in result_files:
            result_dataset_schema = load_dataset(str(result_file))
            convert_result_dataset_to_models(result_dataset_schema, session)

if __name__ == "__main__":
    main()