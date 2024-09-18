from motor.motor_asyncio import AsyncIOMotorClient
from app.Utils.config import settings, get_password_hash
from pymongo.errors import ServerSelectionTimeoutError


async def check_and_create_db():
    try:
        client = AsyncIOMotorClient(settings.mongo_url)
        db_name = settings.mongo_db_name
        await client.server_info()

        db_list = await client.list_database_names()
        print(f"Connection Established.\n\n\n")

        if db_name in db_list:
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Database '{db_name}' doesn't exist. Creating it.")
            db = client[db_name]
            
            users_collection = db["users"]
            
            admin_user = await users_collection.find_one({"username": "admin"})
            if not admin_user:
                hashed_password = get_password_hash("admin")
                await users_collection.insert_one({
                    "username": "admin",
                    "hashed_password": hashed_password
                })
                print("Admin user created with username: 'admin' and password: 'admin'.")
            else:
                print("Admin user already exists.")
        
    except ServerSelectionTimeoutError as err:
        print("Failed to connect to MongoDB:", err)


class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongo_url)
        self.db = self.client[settings.mongo_db_name]

    def get_collection(self, name: str):
        return self.db[name]

db_instance = Database()


async def get_database():
    return db_instance
