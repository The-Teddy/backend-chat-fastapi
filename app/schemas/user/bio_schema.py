from pydantic import BaseModel, field_validator
from app.validators import validate_bio

class BioSchema(BaseModel):
    bio: str

    @field_validator('bio')
    def validation_bio(bio: str)-> str:
        return validate_bio(bio)
