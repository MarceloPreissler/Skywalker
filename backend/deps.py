from fastapi import Depends, Header, HTTPException, status

from .config import get_settings


async def verify_api_key(x_api_key: str = Header(..., alias="x-api-key")) -> None:
    settings = get_settings()
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
