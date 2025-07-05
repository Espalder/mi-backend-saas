from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    rol: str
    empresa_id: int

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    empresa_id: Optional[int] = None 