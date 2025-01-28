# Модель пользователя

from fastapi import FastAPI, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

users = []

class User(BaseModel):
    id: Annotated[int, Field(gt=0, description='Enter id')]
    username: Annotated[str, Field(min_length=5, max_length=20, description='Enter  username')]
    age: Annotated[int, Field(gt=18, le=120, description='Enter age')]

@app.get("/")
async def root() -> str:
    return "Добро пожаловать в API"

@app.get("/users")
async def get_users() -> list[dict]:
    return users

@app.post("/user/{username}/{age}")
async def post_user(user: User, username: str, age: int) -> list:
    user.id = users[len(users)-1]["id"] + 1 if users else 1
    user.username = username
    user.age = age
    users.append({"id": user.id, "username": user.username, "age": user.age})
    return [{"id": user.id, "username": user.username, "age": user.age}]

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int) -> dict:
    for i in range(len(users)):
        user = users[i]
        if user["id"] == user_id:
            user["username"] = username
            user["age"] = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int ) -> dict:
    for user in users:
        if user["id"] == user_id:
            del_user = users.pop(user_id-1)
            return del_user
    raise HTTPException(status_code=404, detail="User was not found")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)