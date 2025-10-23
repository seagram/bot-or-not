import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import msgspec
import os
from sqlmodel import create_engine, SQLModel, Session, delete
from dotenv import load_dotenv
from schemas.schemas import ResultDataset as ResultDatasetSchema
from models.models import Post, User, Detector

result_decoder = msgspec.json.Decoder(ResultDatasetSchema)

def load_dataset(file_path: str):
    with open(file_path, "r") as f:
        content = f.read()
        return result_decoder.decode(content)

def convert_result_dataset_to_models(schema_dataset: ResultDatasetSchema, session: Session, batch_size: int = 1000):
    users_to_add = []
    detectors_to_add = []

    print(f"processing {len(schema_dataset.users)} users...")
    for user_schema in schema_dataset.users:
        bot_team_id = int(user_schema.bot_team_id) if isinstance(user_schema.bot_team_id, str) else user_schema.bot_team_id

        user = User(
            id=user_schema.user_id,
            tweet_count=user_schema.tweet_count,
            z_score=user_schema.z_score,
            username=user_schema.username,
            name=user_schema.name,
            description=user_schema.description,
            location=user_schema.location,
            is_bot=user_schema.is_bot,
            bot_team_id=bot_team_id,
            bot_team_name=user_schema.bot_team_name
        )
        users_to_add.append(user)

        for detector_schema in user_schema.detectors:
            detector = Detector(
                user_id=user_schema.user_id,
                team_name=detector_schema.teamName,
                is_bot=detector_schema.isBot,
                confidence=detector_schema.confidence
            )
            detectors_to_add.append(detector)

    user_batches = [users_to_add[i:i + batch_size] for i in range(0, len(users_to_add), batch_size)]
    for idx, batch in enumerate(user_batches, 1):
        session.add_all(batch)
        session.commit()
        print(f"committed user batch {idx}/{len(user_batches)} ({len(batch)} users)")

    detector_batches = [detectors_to_add[i:i + batch_size] for i in range(0, len(detectors_to_add), batch_size)]
    for idx, batch in enumerate(detector_batches, 1):
        session.add_all(batch)
        session.commit()
        print(f"committed detector batch {idx}/{len(detector_batches)} ({len(batch)} detectors)")

    posts_to_add = []
    print(f"processing {len(schema_dataset.posts)} posts...")
    for post_schema in schema_dataset.posts:
        post = Post(
            id=post_schema.id,
            author_id=post_schema.author_id,
            text=post_schema.text,
            created_at=post_schema.created_at,
            lang=post_schema.lang
        )
        posts_to_add.append(post)

    post_batches = [posts_to_add[i:i + batch_size] for i in range(0, len(posts_to_add), batch_size)]
    for idx, batch in enumerate(post_batches, 1):
        session.add_all(batch)
        session.commit()
        print(f"committed post batch {idx}/{len(post_batches)} ({len(batch)} posts)")

def main():
    load_dotenv()
    db_url = os.environ.get("TURSO_DATABASE_URL")
    db_token = os.environ.get("TURSO_AUTH_TOKEN")
    if not db_url:
        raise ValueError("TURSO_DATABASE_URL environment variable is not set")
    if not db_token:
        raise ValueError("TURSO_AUTH_TOKEN environment variable is not set")

    print("connecting to Turso database...")
    engine = create_engine(
        f"sqlite+{db_url}?secure=true",
        connect_args={
            "auth_token": db_token,
        },
        echo=False,
        pool_pre_ping=True,
    )
    print("connected.\n")

    SQLModel.metadata.create_all(engine)
    data_dir = Path(__file__).parent.parent / "data"
    result_file = data_dir / "results_dataset_1.json"

    with Session(engine) as session:
        print("deleting existing database data...")
        session.exec(delete(Detector))
        session.exec(delete(Post))
        session.exec(delete(User))
        session.commit()
        print("deleted.\n")

        print(f"processing file: {result_file.name}")
        result_dataset_schema = load_dataset(str(result_file))
        convert_result_dataset_to_models(result_dataset_schema, session)
        print("\ndone.")

if __name__ == "__main__":
    main()