from app.models import TokenModel
from app.repositories import TokenRepository
from datetime import datetime, timedelta, timezone
from jose import jwt
from os import getenv

class TokenService:


    def __init__(self,):
        self.secret_key     = getenv("SECRET_KEY")
        self.algorithm      = "HS256"
        self.expire_minutes = 144000
        self.repository     = TokenRepository()

    async def insert_token_and_email(self, data: TokenModel):
        data = data.model_dump()
        data.pop("id")

        result = await self.repository.insert_one(data)
        return str(result.inserted_id)


    async def create_access_token(self, data: dict, expires_delta: timedelta = None, insert: bool = False):
        
        to_encode = data.copy()
        expire  = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self.expire_minutes))
        to_encode.update({"exp": expire})
        to_encode.pop('name')

        jwt_token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        if insert:
            await self.insert_token_and_email(TokenModel(email=data['email'], token=jwt_token, name=data['name']))


        return jwt_token
        
    async def update_token_and_send_email(self, token: str)-> None:
        result = await self.repository.find_one_by_token(token)
        if not result:
            raise ValueError("Token inválido")
        
        new_token = await self.create_access_token({"email": result['email'], "name": result['name']}, timedelta(minutes=60))
        await self.repository.update_one_by_token(token, new_token)

        from app.services import EmailService
        await EmailService().send_email("Para ativar sua conta", "Verificação de e-mail", result['email'], result['name'], new_token, True)

    
    async def delete_token_by_email(self, email: str):
        return await self.repository.delete_one_by_email(email)

    async def get_user_by_token(self,token: str)-> dict:

        return jwt.decode(token, self.secret_key, algorithms=self.algorithm)