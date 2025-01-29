# Список пользователей в шаблоне

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel, Field


# не использовать кнопку "Try it out" и включить режим отладки
#app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins="origins", allow_methods="*")

# расположение шаблонов Jinja2
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: Annotated[int, Field(gt=0, description='Enter id')]
    username: Annotated[str, Field(min_length=5, max_length=20, description='Enter  username')]
    age: Annotated[int, Field(gt=18, le=120, description='Enter age')]


@app.get(path="/", response_class=HTMLResponse)
async def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get(path="/user/{user_id}", response_class=HTMLResponse)
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int ) -> dict:
    for user in users:
        if user["id"] == user_id:
            del_user = users.pop(user_id-1)
            return del_user
    raise HTTPException(status_code=404, detail="User was not found")

@app.post(path="/user/{username}/{age}")
async def post_user(user: User, username: str, age: int) -> list:
    user.id = users[len(users)-1]["id"] + 1 if users else 1
    user.username = username
    user.age = age
    users.append({"id": user.id, "username": user.username, "age": user.age})
    #users.append(user)
    print(users[user.id])
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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)