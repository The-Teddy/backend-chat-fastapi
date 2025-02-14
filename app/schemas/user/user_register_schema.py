from pydantic import BaseModel, field_validator
from app.validators import NAME_REGEX, USERNAME_REGEX, EMAIL_REGEX, PASSWORD_REGEX
import re

class UserRegisterSchema(BaseModel):

    name: str
    username: str
    email: str
    password: str

    @field_validator('name')
    def validate_name(name: str)-> str:

        if not re.match(NAME_REGEX, name):
            raise ValueError("O nome deve ter entre 3 e 100 caracteres e conter apenas letras (incluindo acentuadas) e espaços")

        return name
    
    @field_validator('username')
    def validate_username(username: str)-> str:

        if not re.match(USERNAME_REGEX, username):
            raise ValueError("O nome de usuário deve ter entre 3 e 50 caracteres, sem espaços, contendo apenas letras de A a Z e números.")
        
        return username
    
    @field_validator('email')
    def validate_email(email: str) -> str:

        if not re.match(EMAIL_REGEX, email):
            raise ValueError("O e-mail inserido é inválido. Certifique-se de que ele está no formato correto (exemplo: usuario@dominio.com) e não contém espaços ou caracteres especiais não permitidos.")

        return email
    
    @field_validator('password')
    def validate_password(password: str)-> str:

        if not re.match(PASSWORD_REGEX, password):
            raise ValueError("A senha deve ter entre 8 e 30 caracteres e incluir pelo menos uma letra maiúscula, uma letra minúscula, um número e um caractere especial.")

        return password
