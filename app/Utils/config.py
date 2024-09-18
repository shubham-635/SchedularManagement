from pydantic_settings import BaseSettings
from pydantic import BaseModel
from datetime import datetime
import os
from passlib.context import CryptContext

# Load environment variables from **.env** file
if not os.getenv("APP_ENV"):
    from dotenv import load_dotenv
    load_dotenv(".env")


class Job(BaseModel):
    name: str
    interval: int  # Interval in minutes
    next_run: datetime


class Settings(BaseSettings):
    mongo_url: str = os.getenv('MONGODB_URI')
    mongo_db_name: str = os.getenv('MONGODB_NAME')
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM')
    access_token_expire_minutes: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60))


settings = Settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)
