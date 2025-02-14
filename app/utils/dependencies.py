from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from os import getenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        SECRET_KEY = getenv('SECRET_KEY')
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = payload.get('sub')

        if not user:
            raise HTTPException(status_code=401, detail={"errors": "Token inválido"})
        return user
    
    except JWTError as error:
        raise HTTPException(status_code=401, detail={"errors": "Token inválido"})