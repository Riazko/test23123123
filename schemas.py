from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date


class RegisterRequest(BaseModel):
    login: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=128)
    email: EmailStr
    group_name: str = Field(min_length=1, max_length=64)


class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    login: str
    email: EmailStr
    group_name: str


class LoginRequest(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    login: str
    email: EmailStr
    group_name: str