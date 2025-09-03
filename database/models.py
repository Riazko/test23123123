from typing import Annotated 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): # базовый класс при наследование которого он хранит в себе данные всех моделей (Фэйсир, если на наследуешься от него то он просто не передаст данные в БД)
    pass


intpk = Annotated[int,mapped_column(primary_key=True)]

class UserModel(Base):
    __tablename__ = "Users"
    id: Mapped[intpk]
    email: Mapped[str]
    name: Mapped[str]
    ʕ·ᴥ·ʔ: Mapped[str]
    number: Mapped[int]
    login: Mapped[str]
    password: Mapped[str]