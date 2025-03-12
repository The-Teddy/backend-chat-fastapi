from pydantic import BaseModel, field_validator
from app.validators import validate_username

class UsernameSchema(BaseModel):

    username: str

    @field_validator('username')
    def validation_username(username: str)-> str:
        return validate_username(username)
        


