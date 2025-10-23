import os
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from functools import lru_cache

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@lru_cache(maxsize=1)
def get_valid_api_keys() -> set[str]:
    api_keys_env = os.getenv("API_KEYS", "")
    return set(key.strip() for key in api_keys_env.split(",") if key.strip())

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )

    valid_keys = get_valid_api_keys()

    if not valid_keys:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No API keys configured"
        )

    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    return api_key
