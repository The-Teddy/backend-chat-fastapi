from app.config import mongodb
from bson import ObjectId
from typing import Optional
from datetime import datetime, timezone
from pymongo import ReturnDocument

class UserRepository:

   
    async def insert_user(self, user_data: dict):
        return await mongodb.db.users.insert_one(user_data)
    
    async def find_user_by_email(self, email: str)-> Optional[dict]:
        return await mongodb.db.users.find_one({"email": email})
    
    async def find_user_by_username(self, username: str)-> Optional[dict]:        
        return await mongodb.db.users.find_one({"username": username})

    async def find_user_by_id(self, id: str)-> Optional[dict]:        
        return await mongodb.db.users.find_one({"_id": ObjectId(id)})
    
    async def find_users(self) -> list[dict]:
        return await mongodb.db.users.find().to_list()
    
    async def verify_email(self, email: str)-> bool:
        result = await mongodb.db.users.update_one({"email": email}, {"$set": {"email_verified": datetime.now(timezone.utc)}})
        return result.modified_count > 0
    
    async def delete_user_by_id(self, id: ObjectId)-> bool:
        result = await mongodb.db.users.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    async def delete_user_by_email(self, email: str)-> bool:
        result = await mongodb.db.users.delete_one({"email": email})
        return result.deleted_count > 0
    
    async def update_profile_photo(self, photo: str, id: str)-> dict:
        data = {"photo": photo, "updated_at": datetime.now(timezone.utc)}
        return await mongodb.db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": data}, return_document=ReturnDocument.AFTER)
    
    async def update_name(self, name: str, id: str)-> dict:
        data = {"name": name, "updated_at": datetime.now(timezone.utc)}

        return await mongodb.db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": data}, return_document=ReturnDocument.AFTER)

    async def update_bio(self, bio: str, id: str)-> dict:
        data = {"bio": bio, "updated_at": datetime.now(timezone.utc)}

        return await mongodb.db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": data}, return_document=ReturnDocument.AFTER)