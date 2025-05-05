from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class AdminUserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str] 

class AdminUserCreate(AdminUserBase):
    password: str
    email: EmailStr
    role: str 

class AdminUserUpdate(AdminUserBase):
    pass

class AdminUserOut(AdminUserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)