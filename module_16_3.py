# Имитация работы с БД
from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1' : 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_users() -> dict:
    return users

@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')]
                    , age: Annotated[int, Path(gt=18, le=100, description='Enter age', example='49')]) -> str:
    user_id = str(int(max(users, key=int)) + 1)
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return (f"User {user_id} is registered")

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(gt=0, description='Enter User ID', example='11')]
                      , username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')]
                    , age: Annotated[int, Path(gt=18, le=100, description='Enter age', example='49')]) -> str:
    if user_id in users:
        users[str(user_id)] = f"Имя: {username}, Возраст: {age}"
    else:
        return f"The user {user_id} not found"
    return f"The user {user_id} is updated"

@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    if user_id in users:
        del users[str(user_id)]
    else:
        return f"The user {user_id} not found"
    return f"The user {user_id} is deleted"
