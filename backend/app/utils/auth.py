from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt  # pyright: ignore[reportMissingModuleSource]
from passlib.context import CryptContext  # pyright: ignore[reportMissingModuleSource]
from fastapi import HTTPException, status, Depends # pyright: ignore[reportMissingImports]
from fastapi.security import OAuth2PasswordBearer # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]
from app.database.db_session import get_db
from app.database import models_chat as models

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

JWT_TOKEN = os.getenv("JWT_TOKEN_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password[:72])

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generate a short-lived JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """Generate a long-lived JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_TOKEN, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status = 401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status = 401, detail="Invalid token")
    

# Current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Extract current user from JWT and fetch from DB.
    """
    try:
        payload = jwt.decode(token, JWT_TOKEN, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = db.query(models.Users).filter(models.Users.username == username).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
