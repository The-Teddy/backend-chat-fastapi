from app.config import mongodb

async def create_user_indexies():
    await mongodb.db.users.create_index("username", unique=True)
    await mongodb.db.users.create_index("email", unique=True)
    await mongodb.db.users.create_index("id", unique=True)
