from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RoleUpdate(BaseModel):
    id: int
    email: EmailStr
    role: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"