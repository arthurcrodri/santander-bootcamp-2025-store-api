# store/core/db.py

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.core.config import settings
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation


class MongoClient:
    def __init__(self):
        self.codec_options = CodecOptions(uuid_representation=UuidRepresentation.STANDARD)

        self.client = AsyncIOMotorClient(
            settings.MONGO_URL, uuidRepresentation="standard"
        )

    def get_database(self) -> AsyncIOMotorDatabase:
        return self.client.get_database("store", codec_options=self.codec_options)


db_client = MongoClient()