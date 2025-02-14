from app.models import UserModel
from app.repositories import UserRepository
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from app.schemas import UserRegisterSchema

class UserService:

    user_repository = UserRepository()
    
    async def create_user(self, user: UserRegisterSchema):
        try:
            user_data = user.model_dump()
            user_dict = UserModel(**user_data).model_dump()
            user_dict.pop('id')

            user_email_found    = await self.user_repository.find_user_by_email(user_dict['email'])
            if user_email_found:
                raise HTTPException(status_code=409, detail={"errors": "O E-mail escolhido já está em uso"})

            from app.services import AuthService
            user_dict['password'] = await AuthService().generate_hash_password(user_dict['password'])
            
            result = await self.user_repository.insert_user(user_dict)
            return str(result.inserted_id)
        
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail={"message": "nome de usuário já está em uso."})
    
    async def get_user_by_username(self, username: str)-> str:

        return await self.user_repository.find_user_by_username(username)


