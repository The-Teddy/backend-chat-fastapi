from pydantic import BaseModel, Field
from datetime import datetime

class TokenModel(BaseModel):

    id: str = None
    name: str   = Field(str, max_length=100)
    email: str  = Field(str, max_length=255)
    token: str  = Field(str, max_length=144) 
    created_at: datetime  = Field(default_factory=datetime.now)

