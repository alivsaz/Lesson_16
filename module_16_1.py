from fastapi import FastAPI, HTTPException

app = FastAPI(encodings=['utf-8'])

@app.get("/")
async def get_main_page():
    return "Главная страница"

@app.get("/user/admin")
async def get_admin_page():
    return "Вы вошли как администратор"

@app.get("/user/{user_id}")
async def get_user_number(user_id: int):
    return f"Вы вошли как пользователь № {user_id}"

@app.get("/user")
async def get_user_info(username: str, age: int):
    return f"Информация о пользователе. Имя: {username}, Возраст {age}."