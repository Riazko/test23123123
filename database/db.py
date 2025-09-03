import datetime
from typing import Annotated
import uuid
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

"""from database.models import ChatModel, MessageModel, UserModel"""


engine = create_async_engine('sqlite+aiosqlite:///KONFETA.db')   # Указываем параметры что база данных это sqlite, asynс работа с БД (откройте кассу), где распалагается 
new_session = async_sessionmaker(engine, expire_on_commit=False) # создаем новую сессию, expire_on_commit=False - что бы он не отправлял коммиты

async def get_session():
    async with new_session()as session: # переименовываем  async with new_session() в session
        yield session   #  yield - фунгия пайтона котрая создает генератьор
        
SessionDep = Annotated[AsyncSession,Depends(get_session)] # мы создаем иньекцию зависимости для FastAPI что он автоматически вызывал get_session, 
# ибез Depends мне бы пришлось открывать и закрывать сессию для базы данных, метод из FastAPI




