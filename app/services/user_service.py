from app.models import UserModel
from app.repositories import UserRepository
from pymongo.errors import DuplicateKeyError
from app.schemas import UserRegisterSchema
from app.utils.utils import to_iso_format
from datetime import timedelta
from os import remove, path

class UserService:

    def __init__(self,):
        from app.services import EmailService, TokenService

        self.repository     = UserRepository()
        self.email_service  = EmailService()
        self.token_service  = TokenService()

    
    async def create_user(self, user: UserRegisterSchema):
        try:
            user_data = user.model_dump()
            user_dict = UserModel(**user_data).model_dump()
            user_dict.pop('id')
            
            from app.services import AuthService
            user_dict['password'] = await AuthService().generate_hash_password(user_dict['password'])

            result = await self.repository.insert_user(user_dict)
            print("Usuário criado com sucesso")
            TOKEN = await self.token_service.create_access_token({"email": user_dict['email'], "name": user_dict['name']}, timedelta(minutes=60), True)

            await self.email_service.send_email("Para ativar sua conta" , "Verificação de e-mail", user_dict['email'], user_dict['name'], TOKEN, False)
            return str(result.inserted_id)
        
        except DuplicateKeyError as error:            
            error  = str(error)
            if 'email' in error:
                print("error: O e-mail escolhido já está em uso")
                raise DuplicateKeyError("O E-mail escolhido já está em uso")
            
            if 'username' in error:
                print("error: nome de usuário já está em uso.")
                raise DuplicateKeyError("O nome de usuário já está em uso.")     
    
    async def get_user_by_username(self, username: str)-> dict:
        return await self.repository.find_user_by_username(username)
    
    async def get_user_by_email(self, email: str)-> dict:
        found_user = await self.repository.find_user_by_email(email)
        if not found_user:
            return None
        
        found_user['id'] = str(found_user['_id'])

        user = UserModel(**found_user).model_dump()
        user = to_iso_format(user)
        return user
    
    async def verify_email_user(self, email: str)-> bool:

        updated = await self.repository.verify_email(email)

        if updated:
            await self.token_service.delete_token_by_email(email)
            return True
        return False
    
    async def update_profile_photo_user(self, path_photo: str, id: str)-> dict:
        try:
            found_user      = await self.repository.find_user_by_id(id)

            old_path_photo = found_user['photo']

            updated_user    = await self.repository.update_profile_photo(str(path_photo), id)
            updated_user    = to_iso_format(updated_user)

            if path.exists(old_path_photo):
                remove(old_path_photo)
            
            data = {"photo": updated_user['photo'], "updated_at": updated_user['updated_at']}
            return data

        except Exception as error:
            print(f"Erro ao trocar de foto no service: {error}")
            if path.exists(path_photo):
                remove(path=path_photo)
            raise Exception(error)

    async def update_name(self, name: str, id: str)-> dict:
        
        updated_user = await self.repository.update_name(name, id)
        if not updated_user:
            return None

        data = {"name": updated_user['name'], "updated_at": updated_user['updated_at']}
        data = to_iso_format(data)
        return data
    
    async def update_bio(self, bio: str, id: str)-> dict:

        updated_user = await self.repository.update_bio(bio, id)
        if not updated_user:
            return None
        
        data = {"bio": updated_user['bio'], "updated_at": updated_user['updated_at']}
        data = to_iso_format(data)
        return data
        
       




