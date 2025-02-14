from passlib.context import CryptContext

class AuthService:

    bcrypt: CryptContext = CryptContext(schemes=['bcrypt'], deprecated="auto")

    async def generate_hash_password(self, password: str)-> str:
        return self.bcrypt.hash(password)
    
    async def check_password(self, email: str, password: str)-> bool:
        return self.bcrypt.verify(password)