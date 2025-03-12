from pydantic import BaseModel, field_validator
from app.validators import validate_name

class NameSchema(BaseModel):
    
    name: str

    @field_validator('name')
    def validation_name(name: str) -> str:
        return validate_name(name)