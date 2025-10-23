import os
import boto3
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from functools import lru_cache

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@lru_cache(maxsize=1)
def get_ssm_client():
    return boto3.client('ssm')

@lru_cache(maxsize=1, ttl=300)
def get_valid_api_keys() -> set[str]:
    param_name = os.getenv("API_KEYS_PARAM_NAME")

    if not param_name:
        api_keys_env = os.getenv("API_KEYS", "")
        return set(key.strip() for key in api_keys_env.split(",") if key.strip())

    try:
        ssm = get_ssm_client()
        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
        api_keys_value = response['Parameter']['Value']
        return set(key.strip() for key in api_keys_value.split(",") if key.strip())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve API keys: {str(e)}"
        )

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
