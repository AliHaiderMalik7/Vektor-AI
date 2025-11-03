from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import models_chat as models
from app.database.db_session import get_db
from app.utils.auth import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.models.request_models import UserSignupRequest, UserLoginRequest , TokenResponse

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sign up

@router.post("/signup")
def signup(request: UserSignupRequest, db: Session = Depends(get_db)):
    # Check for existing email or username
    if db.query(models.Users).filter(models.Users.email == request.email).first():
        raise HTTPException(status=400, detail="Email already exists")
    if db.query(models.Users).filter(models.Users.username == request.username).first():
        raise HTTPException(status=400, detail="Username already exists")

    # Hash password
    hashed_password = get_password_hash(request.password)
    user = models.Users(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        username=request.username,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"status": 201, "message": "User created successfully", "user_id": user.id}

# Login

@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    # Looking for a user in database    
    user = db.query(models.Users).filter(models.Users.username == request.username).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status=401, detail="Invalid credentials")
    
    # Token Generate
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return TokenResponse(status = 200, message = "Login Successful",access_token=access_token, refresh_token=refresh_token)