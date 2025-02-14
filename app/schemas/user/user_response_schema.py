from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class UserResponseSchema(BaseModel):

    id: Optional[str]                   
    name: str                          
    username: str                      
    email: str                          
    status: Optional[str]               
    last_login: Optional[datetime]      
    email_verified: Optional[datetime] 
    is_active: bool                     
    role: str                           
    contacts: List[str]                 
    blockeds: List[str]                 
    created_at: datetime                
    updated_at: datetime                