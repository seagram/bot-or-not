api:
    cd ./src
    uv run uvicorn server:app --reload

seed:
    cd ./scripts
    uv run seed.py