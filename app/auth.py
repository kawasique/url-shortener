from typing import Annotated
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from settings import API_KEY


api_key_scheme = APIKeyHeader(name="x-api-key")


async def verify_key(api_key: Annotated[str, Security(api_key_scheme)]):
    if api_key != API_KEY:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="Invalid api_key")
