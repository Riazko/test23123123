import uuid
from sqlalchemy import Column, Integer, String, Date
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # автоинкремент
    user_id = Column(String, unique=True, index=True, nullable=False) # публичный UUID
    login = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    group_name = Column(String, nullable=False)

    @staticmethod
    def generate_user_id() -> str:
        return str(uuid.uuid4())