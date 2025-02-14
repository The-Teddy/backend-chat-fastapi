from app.models import UserModel
from app.repositories import UserRepository
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from app.schemas import UserRegisterSchema
from app.utils.utils import to_iso_format

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
    
    async def get_user_by_username(self, username: str)-> dict:
        return await self.user_repository.find_user_by_username(username)
    
    async def get_user_by_email(self, email: str)-> dict:
        found_user = await self.user_repository.find_user_by_email(email)
        found_user['id'] = str(found_user['_id'])

        user = UserModel(**found_user).model_dump()
        user = to_iso_format(user)
        return user




