from jose.exceptions import JWTError
from jose import jwt

from fastapi import Depends, HTTPException, status

from app.schemas.response import UserResponse
from config.database import get_db
from app.models.models import User
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from config.settings import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token:str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_uid: str = payload.get("sub")
        if user_uid is None:
            raise credentials_exception
        user = session.query(User).filter(User.uid == user_uid).first()
    except JWTError:
        raise credentials_exception

    if user is None:
        raise credentials_exception
    return user

