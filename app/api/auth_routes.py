from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import auth as auth_schemas
from app.schemas import user as user_schemas
from app.infrastructure.repositories.auth_repository import AuthHandler
from app.infrastructure.repositories.user_repository import UserRepository
from app.api.dependencies import get_db

router = APIRouter()

auth_handler = AuthHandler()

@router.post("/register/", response_model=user_schemas.User)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth_handler.hash_password(user.password)
    user_in_db = user_schemas.UserCreate(name=user.name, email=user.email, password=hashed_password)
    new_user = userRepository.create_user(user=user_in_db)
    return new_user

@router.post("/login/", response_model=auth_schemas.Token)
def login(form_data: auth_schemas.UserLogin, db: Session = Depends(get_db)):
    userRepository = UserRepository(db)
    user = userRepository.get_user_by_email(form_data.email)
    if user is None or not auth_handler.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = auth_handler.create_access_token(data={"sub": user.email})
    refresh_token = auth_handler.create_refresh_token(data={"sub": user.email})
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh/", response_model=auth_schemas.Token)
def refresh_token(token: auth_schemas.TokenRefresh):
    email = auth_handler.decode_refresh_token(token.refresh_token)
    access_token = auth_handler.create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}
