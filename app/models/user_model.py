from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] 
    name: str                           = Field(min_length=3, max_length=100)
    username: str                       = Field(min_length=3, max_length=50)
    email: str                          = Field(max_length=255)
    password: str                       = Field(max_length=255)
    photo: Optional[str]                = Field(default=None, max_length=255)
    status: Optional[str]               = Field(default=None, max_length=50)
    bio: Optional[str]                  = Field(default=None, max_length=300)
    last_login: Optional[datetime]      = None
    email_verified: Optional[datetime]  = None
    is_active: bool                     = True
    role: str                           = "user"

    contacts: List[str]                 = Field(default=[])
    blockeds: List[str]                 = Field(default=[])
    created_at: datetime                = Field(default_factory=datetime.now)
    updated_at: datetime                = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Convertendo para string ISO
        }

    
    
