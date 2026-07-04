import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

security = HTTPBearer()

class AuthHandler:
    @staticmethod
    def get_password_hash(password: str) -> str:
        # Convert password to bytes, generate a salt, and hash it natively
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Check plain text input against stored hashed bytes natively
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False

    @staticmethod
    def create_access_token(user_id: int, role: str) -> str:
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            return {"user_id": int(payload.get("sub")), "role": payload.get("role")}
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token or session expired")