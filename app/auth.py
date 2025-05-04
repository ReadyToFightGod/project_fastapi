from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str):
    to_encode = {"sub": username}
    expire = (datetime.now(timezone.utc)
              + timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode,
                             settings.secret_key,
                             algorithm=settings.algo)
    return encoded_jwt


def get_token_user(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algo])
    except InvalidTokenError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            e.args[0])
    return payload["sub"]
