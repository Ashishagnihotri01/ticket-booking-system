from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.middleware.auth_handler import AuthHandler
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Authentication"])

# 1. Define what data the endpoint expects
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.CUSTOMER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 2. Add 'user_data: UserRegister' so FastAPI knows to create a Request Body
@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = AuthHandler.get_password_hash(user_data.password)
    new_user = User(name=user_data.name, email=user_data.email, password_hash=hashed_pwd, role=user_data.role)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not AuthHandler.verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = AuthHandler.create_access_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer"}