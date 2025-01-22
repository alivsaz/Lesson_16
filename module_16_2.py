# Аннотация и валидация

from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI(encodings=['utf-8'])

@app.get("/")
async def get_main_page():
    return "Главная страница"

@app.get("/user/admin")
async def get_admin_page():
    return "Вы вошли как администратор"

@app.get("/user/{user_id}")
async def get_user_number(user_id: Annotated[(int, Path(gt=0, le=100, description='Enter User ID', example='27'))]):
    return f"Вы вошли как пользователь № {user_id}"

@app.get("/user/{username}/{age}")
async def get_user_info(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')]
                        , age: Annotated[int, Path(gt=18, le=120, description='Enter age', example='49')]):
    return f"Информация о пользователе. Имя: {username}, Возраст {age}."