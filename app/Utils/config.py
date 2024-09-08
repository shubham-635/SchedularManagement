from pydantic_settings import BaseSettings
from pydantic import BaseModel
from datetime import datetime


class Job(BaseModel):
    name: str
    interval: int  # Interval in minutes
    next_run: datetime

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_name: str = "scheduler_db"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
