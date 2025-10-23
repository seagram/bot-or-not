from sqlmodel import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get("TURSO_DATABASE_URL")
db_token = os.environ.get("TURSO_AUTH_TOKEN")

if not db_url:
    raise ValueError("TURSO_DATABASE_URL environment variable is not set")
if not db_token:
    raise ValueError("TURSO_AUTH_TOKEN environment variable is not set")

engine = create_engine(
    f"sqlite+{db_url}?secure=true",
    connect_args={
        "auth_token": db_token,
    },
    echo=True,
    pool_pre_ping=True,
)