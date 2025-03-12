import re
import bleach
from app.validators import USERNAME_REGEX, NAME_REGEX, EMAIL_REGEX, PASSWORD_REGEX, BIO_REGEX


def validate_username(username: str)-> str:

    username = bleach.clean(username.strip(), tags=[], strip=True)

    if not re.match(USERNAME_REGEX, username):
        raise ValueError("O nome de usuário deve ter entre 3 e 25 caracteres, sem espaços, contendo apenas letras de A a Z e números.")
        
    return username

def validate_name(name: str)-> str:
    name = bleach.clean(name.strip(), tags=[], strip=True)

    if not re.match(NAME_REGEX, name):
        raise ValueError("O nome deve ter entre 3 e 30 caracteres e conter apenas letras (incluindo acentuadas) e espaços")

    return name

def validate_email(email: str) -> str:
    email = bleach.clean(email.strip(), tags=[], strip=True)

    if not re.match(EMAIL_REGEX, email):
        raise ValueError("O e-mail inserido é inválido. Certifique-se de que ele está no formato correto (exemplo: usuario@dominio.com) e não contém espaços ou caracteres especiais não permitidos.")

    return email

def validate_password(password: str)-> str:
    password = bleach.clean(password.strip(), tags=[], strip=True)

    if not re.match(PASSWORD_REGEX, password):
        raise ValueError("A senha deve ter entre 8 e 30 caracteres e incluir pelo menos uma letra maiúscula, uma letra minúscula, um número e um caractere especial.")

    return password

def validate_bio(bio: str)-> str:
    bio = bleach.clean(bio.strip(), tags=[], strip=True)

    if not re.match(BIO_REGEX, bio):
        raise ValueError("A bio deve ter entre 10 e 200 caracteres.")
    return bio