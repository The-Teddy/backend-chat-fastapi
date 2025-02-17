from passlib.context import CryptContext
from fastapi import HTTPException
from app.utils import create_access_token

class AuthService:

    bcrypt: CryptContext = CryptContext(schemes=['bcrypt'], deprecated="auto")

    async def generate_hash_password(self, password: str)-> str:
        return self.bcrypt.hash(password)
    
    async def check_password(self, hash_password: str, password: str)-> bool:
        return self.bcrypt.verify(password, hash_password) 
    
    async def authenticate_user(self, email: str, password: str)-> dict:
        from app.services import UserService

        found_user = await UserService().get_user_by_email(email)

        if not found_user:
            raise HTTPException(status_code=401, detail={"errors": "Credenciais inválidas"})
        
        if not found_user['is_active']:
            raise HTTPException(status_code=403, detail={"errors": "Usuário inativo"})
        
        if not found_user['email_verified']:
            raise HTTPException(status_code=403, detail={"errors": "E-mail não verificado"})

        if not await self.check_password(found_user['password'], password):
            raise HTTPException(status_code=401, detail={"errors": "Credenciais inválidas"})
        

        found_user.pop('password')
        access_token = await create_access_token(found_user)
        found_user.pop("id")

        return {"access_token": access_token, "data": found_user}


        