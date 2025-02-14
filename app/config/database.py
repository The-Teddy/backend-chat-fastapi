from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv

MONGO_URI = getenv('MONGO_URI')
MONGO_DB  = getenv('MONGO_DB')

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.uri        = uri
        self.db_name    = db_name
        self.client     = None
        self.db         = None

    async def connect(self,):
        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        print("database connected")

    async def disconnect(self,):
        if self.client:
            self.client.close()
            print("database disconnected")

mongodb = MongoDB(MONGO_URI, MONGO_DB)