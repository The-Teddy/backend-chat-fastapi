from pydantic import BaseModel, field_validator
from app.validators import validate_name, validate_email, validate_password, validate_username

class UserRegisterSchema(BaseModel):

    name: str
    username: str
    email: str
    password: str

    @field_validator('name')
    def validation_name(name: str)-> str:
        return validate_name(name)
        
    
    @field_validator('username')
    def validation_username(username: str)-> str:
        return validate_username(username)
       
    
    @field_validator('email')
    def validation_email(email: str) -> str:
        return validate_email(email)
        
    
    @field_validator('password')
    def validation_password(password: str)-> str:
        return validate_password(password)
       