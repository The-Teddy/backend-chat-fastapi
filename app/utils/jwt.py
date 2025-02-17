from datetime import datetime, timedelta
from jose import jwt
from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 144000

async def create_access_token(data: dict, expires_delta: timedelta = None):
    
    to_encode = data.copy()
    expire  = datetime.now() + (expires_delta or timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

