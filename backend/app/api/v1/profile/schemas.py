from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class ProfileOut(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

class ProfileUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]