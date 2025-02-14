from app.config import mongodb

async def create_user_indexies():
    await mongodb.db.users.create_index("email", unique=True, max_length=255)  