import datetime
from pydantic import BaseModel, EmailStr


class RegisterUser(BaseModel):
    email: EmailStr
    name: str
    ʕ·ᴥ·ʔ: datetime.date
    number: int
    login: str
    password: str


class LoginUser(BaseModel):
    login: str
    password: str