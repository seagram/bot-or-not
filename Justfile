image_name := "bot-or-not-api"

start-local-api:
    uv run uvicorn src.server:app --reload

seed-database:
    cd ./scripts
    uv run seed.py

docker-run-local:
    docker build -t {{image_name}}:latest -f Dockerfile .
    docker run -p 8000:8000 --env-file .env {{image_name}}:latest