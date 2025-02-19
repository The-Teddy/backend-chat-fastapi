from app.config import mongodb

class TokenRepository:

    async def insert_one(self, data: dict)-> dict:
        return await mongodb.db.tokens.insert_one(data)
    
    async def find_one_by_token(self, token: str)-> dict:
        return await mongodb.db.tokens.find_one({"token": token})
    
    async def update_one_by_token(self, old_token: str, new_token: str)-> bool:
        result = await mongodb.db.tokens.update_one({"token": old_token}, {"$set": {"token": new_token}})
        print(result)
        return result.modified_count > 0
    
    async def delete_one_by_email(self, email: str)-> bool:
        result = await mongodb.db.tokens.delete_one({"email": email})
        return result.deleted_count > 0