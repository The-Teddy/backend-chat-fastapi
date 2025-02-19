from pydantic import BaseModel

class ResendToken(BaseModel):
    token: str