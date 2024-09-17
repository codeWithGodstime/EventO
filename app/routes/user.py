from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_user
from app.schemas.request import UserRegisterRequest, UserLoginRequest
from app.schemas.response import UserResponse, UserLoginReponse
from app.utils import hash_password, verify_password, generate_tokens
from config.database import get_db
from app.models.models import User
from config.settings import get_settings

settings = get_settings()

auth_router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
    # dependencies=[Depends(get_db)]
)

@auth_router.post("/register", response_model=UserResponse)
def create_account(data: UserRegisterRequest, session: Session = Depends(get_db)):
    hashed_password = hash_password(data.password)
    user = User(username = data.username, email=data.email, password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@auth_router.post("/token", response_model=UserLoginReponse)
def login(data: UserLoginRequest, session: Session=Depends(get_db)):
    user = session.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exists")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    #TODO: check is user account is active or verified

    payload = {"sub": str(user.uid)}
    # generate tokens
    access_token = generate_tokens(
        payload=payload,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        ttl=timedelta(minutes=settings.ACCESS_TOKEN_TTL)
    )
    refresh_token = generate_tokens(
        payload=payload,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        ttl=timedelta(days=settings.REFRESH_TOKEN_TTL),
        is_refresh=True
    )

    user_response = UserResponse(
        uid=str(user.uid),
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        is_organizer=user.is_organizer,
        is_active=user.is_active
    )

    return UserLoginReponse(
        access=access_token,
        refresh=refresh_token,
        data=user_response
    )

@auth_router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    return current_user