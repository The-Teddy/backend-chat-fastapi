from pydantic import BaseModel, field_validator
from app.validators import validate_email, validate_password

class LoginSchema(BaseModel):

    email: str
    password: str

    @field_validator("email")
    def validation_email(email: str)-> str:
        return validate_email(email)
    
    @field_validator('password')
    def validation_password(password: str)-> str:
        return validate_password(password)