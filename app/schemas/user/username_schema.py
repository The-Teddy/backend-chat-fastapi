from pydantic import BaseModel, field_validator
from app.validators import USERNAME_REGEX
import re

class UsernameSchema(BaseModel):

    username: str

    @field_validator('username')
    def validate_username(username: str)-> str:
        if not re.match(USERNAME_REGEX, username):
            raise ValueError("O nome de usuário deve ter entre 3 e 50 caracteres, sem espaços, contendo apenas letras de A a Z e números.")
        
        return username


