# store/core/db.py

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.core.config import settings

class MongoClient:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URL)

    def get_database(self) -> AsyncIOMotorDatabase:
        return self.client.get_database("store")

db_client = MongoClient()