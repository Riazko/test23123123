from datetime import timedelta
import uuid
from authx import AuthX, AuthXConfig # (HS 256(генератор саого длинного пароля в мире который использует все латинские буквы верх. и низ. регистр и все цифры)
#алгоритм который использует authx для создания токена)
from fastapi import HTTPException, Request
from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings): # инструмент для потдержки переменных окружения
    SECRET_KEY:str
    @property                 # ДЕКОРАТОК который не дает доступ к функции или изменению значений внутри нее
    def auth_URL(self):
        return f"{self.SECRET_KEY}"
    
    model_config = SettingsConfigDict(env_file=".env")
    
s = Settings() # экземпляр класс
    
config = AuthXConfig()
config.JWT_SECRET_KEY = s.auth_URL
config.JWT_ACCESS_COOKIE_NAME = "Koki"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=10)

security = AuthX(config=config) # экземпляр класс

