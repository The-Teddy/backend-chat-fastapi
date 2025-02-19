from app.models import UserModel
from app.repositories import UserRepository
from pymongo.errors import DuplicateKeyError
from app.schemas import UserRegisterSchema
from app.utils.utils import to_iso_format
from datetime import timedelta

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
            # print(error)
            
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
        




