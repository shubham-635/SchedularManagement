from motor.motor_asyncio import AsyncIOMotorClient
from app.Utils.config import settings

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_name]

    def get_collection(self, name: str):
        return self.db[name]

db_instance = Database()


async def get_database():
    return db_instance
