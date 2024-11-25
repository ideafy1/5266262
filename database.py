from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGODB_URI)
        self.db = self.client[Config.DB_NAME]
        self.users = self.db["users"]
        self.files = self.db["files"]
        self.clones = self.db["clones"]

    async def add_user(self, user_id: int, username: str = None):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"username": username}},
            upsert=True
        )

    async def add_file(self, file_id: int, user_id: int, timestamp):
        await self.files.insert_one({
            "file_id": file_id,
            "user_id": user_id,
            "timestamp": timestamp
        })

    async def add_clone(self, user_id: int, username: str, bot_token: str, timestamp):
        await self.clones.insert_one({
            "user_id": user_id,
            "username": username,
            "bot_token": bot_token,
            "created_at": timestamp
        })