# """.venv\Scripts\activate                 uvicorn App.main:app --reload"""

from fastapi import FastAPI, HTTPException, Response
from sqlalchemy import select
# Исправляем относительные импорты на абсолютные, если запускаем из корневой директории 
from userr import LoginUser, RegisterUser 
from database.db import engine, SessionDep 
from database.models import Base, UserModel
from AUF.auf import security, config 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request # Добавляем Request

app = FastAPI()

# Вспомогательная функция для декодирования токена и получения ID пользователя
async def get_current_user_id_from_token(request: Request) -> int:
    """
    Извлекает токен из cookie, декодирует его и возвращает ID пользователя.
    Основано на предоставленной пользователем структуре декодирования, адаптировано для AuthX.
    """
    # Шаг 1: Получить токен из cookie
    # Используем config.JWT_ACCESS_COOKIE_NAME, так как это имя устанавливается при входе.
    # В примере пользователя было "my_access_token", но "Koki" (config.JWT_ACCESS_COOKIE_NAME) сконфигурировано и используется.
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    print(f"DEBUG: Токен, полученный из cookie ({config.JWT_ACCESS_COOKIE_NAME}): {token}") # ОТЛАДКА
    if not token:
        # Используем предпочтительное сообщение об ошибке пользователя для отсутствующего cookie токена
        print(f"DEBUG: Cookie токена '{config.JWT_ACCESS_COOKIE_NAME}' не найден.") # ОТЛАДКА
        raise HTTPException(status_code=401, detail="Token cookie not found") # Сообщение от пользователя

    # Шаг 2: Декодировать токен и извлечь ID пользователя
    try:
        print(f"DEBUG: Попытка декодировать токен: {token}") # ОТЛАДКА
        payload = security._decode_token(token)  # объект security из AUF.auf
        print(f"DEBUG: Содержимое токена (payload) после декодирования: {payload}") # ОТЛАДКА
 
        # 'sub' (subject/ID пользователя) находится непосредственно в словаре payload.
        # Строки `user_id_obj = payload.decode(token, "SECRET_KEY")` и `actual_id = user_id_obj.sub`
        # из концептуального кода пользователя здесь неприменимы, так как payload уже является словарем.
        # ИСПРАВЛЕНИЕ: Объект payload (типа TokenPayload) не имеет метода .get().
        # Доступ к 'sub' осуществляется как к атрибуту объекта.
        user_id_str = payload.sub
        

        if user_id_str is None:
            raise HTTPException(status_code=401, detail="ID пользователя (sub) не найден в токене")
        
        return int(user_id_str)  # Предполагаем, что ID пользователя - это int
    except HTTPException: # Повторно вызываем HTTPException, явно созданные (например, sub не найден)
        raise
    except Exception as e: # Ловит ошибки от _decode_token или преобразования в int
        print(f"DEBUG: Ошибка при декодировании токена или извлечении ID: {type(e).__name__} - {e}") # ОТЛАДКА
        # Можно добавить логирование e для отладки: print(f"Ошибка декодирования токена или обработки ID: {e}")
        raise HTTPException(status_code=401, detail="Недействительный токен или не удалось обработать ID пользователя")

origins = [
    "http://127.0.0.1:5500",      # АЗЫ: Сайты деляться на фронтэнд и бэкенд, интернет страничка это - смесь статического содержимого(HTML) и динамического содержимого(JS) которое управляет статическим содержимым
    #которое управляет статическим содержимым . по дефолту браузерам запрещенно передавать какую либо информацию с фронта, для этого и нужны CORS
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Выше список доменов с которых может поступать запрос сфронтэнда заложенных в переменую, allow_origins - разрешает обращаться с всех доменов в списке, если ["*"] - с всех
    allow_credentials=True, #  Если True, то разрешает передачу куки и заголовков авторизации(учетные данные), по умолчанию False
    allow_methods=["*"], # ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"], # определяет, какие HTTP-заголовки разрешено передавать в кросс-доменных запросах . HTTP-заголовки — это часть HTTP-запроса или ответа, которая передает дополнительную информацию между клиентом и сервером
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the UQuest API!"}


@app.post("/setup_database")  # post запрос - потому что мы изменяем нашу систему
async def setup_database():
    async with engine.begin() as conn:  # Обзываем начла
        await conn.run_sync(Base.metadata.drop_all)   # conn - конектимся к базе данных, run-sync - функция sqlalchemy "запустить синхронноб" прикол sqlalchemy потому что раньше она была полностью синхронно, Base.metadata - наследуемся от класса Base в папке модел и metadata - достаем все,  drop_all - очищаем полность базу данных
        await conn.run_sync(Base.metadata.create_all)  # create_all - накатываем новые, пустые таблици
    return f"Ok: {True}"
    
@app.post("/register") # добавление регистрации
async def register(data:RegisterUser,session:SessionDep): # session:SessionDep обращаемся к базе данныз через иньекции зависимо для дольнейшой работы с базой данных
    existing_user = await session.execute(select(UserModel).where(
        (UserModel.email == data.email) |
        (UserModel.login == data.login) |
        (UserModel.number == data.number)
    )) # все что в  () - sql запрос
    if existing_user.scalars().first():  # из базы данных вытаскивает первое совпадение, если такое есть, то выдает ошибку
        raise HTTPException(status_code = 409,detail = "Такой челик уже есть") # raise выводит ошибку, все что в () - описание ошибки
    new_user = UserModel(email = data.email,
                         login = data.login,
                         password = data.password,
                         number = data.number,
                         ʕ·ᴥ·ʔ = data.ʕ·ᴥ·ʔ.isoformat(), # UserModel.ʕ·ᴥ·ʔ ожидает строку
                         name = data.name)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user) # Обновляем объект, чтобы получить ID и другие значения по умолчанию из БД
    return {"success": True, "message": "Пользователь успешно зарегистрирован"}

@app.get("/get_users")
async def get_users(session:SessionDep): # обращаеться к базе данных и вытаскивает всех пользователей
    mr_bear = await session.execute(select(UserModel)) # ждет обращения к базе данных с sql запросом
    return mr_bear.scalars().all() # возвращает все совпадения




@app.post("/login_user")
async def login_user(data:LoginUser,session:SessionDep, response:Response):
    print("--- Login attempt ---")
    print(f"Login data: {data.login}")
    medvedu_slawa = select(UserModel).where(UserModel.login==data.login,UserModel.password==data.password)
    result = await session.execute(medvedu_slawa)
    user = result.scalars().first()

    if user is None:
        print("User not found or password incorrect.") # Отладочный вывод
        raise HTTPException(status_code = 401,detail = "Неправельный логин или пароль, ЧУВАААК")

    print(f"User found: {user.login}, ID: {user.id}") # Отладочный вывод
    token_daun = security.create_access_token(uid = str(user.id))
    print(f"DEBUG: Токен СОЗДАН в /login_user для user_id {user.id}: {token_daun}") # ОТЛАДКА

    try:
        response.set_cookie( # Устанавливаем куку с никнеймом пользователя
            config.JWT_ACCESS_COOKIE_NAME,
            value=token_daun,
            httponly=True,      # Важно для безопасности, cookie недоступен из JavaScript
            samesite='None',    # Необходимо для кросс-доменных запросов с credentials
                                # Требует Secure=True
            secure=True,        # Cookie будет отправляться только по HTTPS.
                                # Для локальной разработки по HTTP это может вызвать проблемы,
                                # т.к. браузер может не установить такой cookie.
                                # Если локально только HTTP, верните secure=False и samesite='Lax'
            path='/'         # Для всего сайта 
        )
        print(f"Cookie '{config.JWT_ACCESS_COOKIE_NAME}' should be set.") # Отладочный вывод
    except Exception as e:
        print(f"Error setting cookie: {e}") # Отладочный вывод, если сама установка cookie вызывает ошибку

    return {"message": "Login successful", "token": token_daun, "user_id": user.id}

@app.get("/profile/{user_id}")
async def get_profile(user_id: int, session: SessionDep):
    user = await session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Возвращаем только те поля, которые есть в UserModel
    return {
        "name": user.name,
        "login": user.login, # Добавляем никнейм в ответ API
        "email": user.email,
    }
  
