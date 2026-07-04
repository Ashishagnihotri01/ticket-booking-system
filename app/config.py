from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENV: str = "development"  # 👈 ADD THIS LINE HERE
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str
    SEAT_HOLD_TTL_SECONDS: int = 600
    WAITLIST_OFFER_TTL_SECONDS: int = 300

    class Config:
        env_file = ".env"
        extra = "ignore"  
settings = Settings()