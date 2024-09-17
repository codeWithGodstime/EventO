import uuid

from pydantic.v1 import UUID4
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone

from jose import jwt

pwd_context = CryptContext(['bcrypt'], deprecated='auto')

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def generate_tokens(payload:dict, secret_key:str, algorithm:str, ttl: timedelta, is_refresh=False):
    current_timestamp = datetime.now(timezone.utc)
    expire = datetime.now(timezone.utc) + ttl
    uid = generate_uid()
    payload.update({
        "exp": expire,
        'jti': str(uid),
        'iat': current_timestamp,
        "type": 'access' if not is_refresh else 'refresh'
    })
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def generate_uid()->str:
    return str(uuid.uuid4())

