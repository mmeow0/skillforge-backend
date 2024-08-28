from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import User
from app.infrastructure.repositories.auth_repository import AuthHandler
from sqlalchemy.orm import Session

auth_handler = AuthHandler()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth_handler = AuthHandler()
    email = auth_handler.decode_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user is None:

        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
