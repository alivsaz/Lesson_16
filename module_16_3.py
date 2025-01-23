# Имитация работы с БД
from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1' : 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_users() -> dict:
    return users

@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', examples='UrbanUser')]
                    , age: Annotated[int, Path(gt=18, le=100, description='Enter age', examples='49')]) -> str:
    user_id = str(int(max(users, key=int)) + 1)
    users[user_id] = f"Имя: {username}, возраст: {str(age)}"
    return f"User {user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(gt=0, description='Enter User ID', examples='11')]
                      , username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', examples='UrbanUser')]
                    , age: Annotated[int, Path(gt=18, le=100, description='Enter age', examples='49')]) -> str:

    users[str(user_id)] = f"Имя: {username}, Возраст: {age}"
    return f"The user {user_id} is updated"

@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    del users[str(user_id)]
    return f"User {user_id} has been deleted"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)