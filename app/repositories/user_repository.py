from app.config import mongodb
from bson import ObjectId
from typing import Optional

class UserRepository:

   
    async def insert_user(self, user_data: dict):
        return  await mongodb.db.users.insert_one(user_data)
    
    async def find_user_by_email(self, email: str)-> Optional[dict]:
        return await mongodb.db.users.find_one({"email": email})
    
    async def find_user_by_username(self, username: str)-> Optional[dict]:        
        return await mongodb.db.users.find_one({"username": username})

    async def find_user_by_id(self, id: str)-> Optional[dict]:        
        return await mongodb.db.users.find_one({"_id": ObjectId(id)})
    
    async def find_users(self) -> list[dict]:
        return await mongodb.db.users.find().to_list()

            