from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import jwt
import datetime

app = FastAPI()

def verify_token(authorization: str = None):

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    else:
        token = authorization

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

class Todo(BaseModel):
    id: int
    title: str
    description: str

todos = []

@app.post("/login")
def login(payload: dict):
    if(payload["username"]=="admin" and payload["password"]=="admin"):

        payload = {
            'user_id': 1,
            'username': 'sample',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30) 
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        return {"message": "Login successful", "token": token}
    else:
        return {"message": "Login failed"}

@app.get("/todos")
def auth_get_todos(authorization: str = Header(None)):
    payload = verify_token(authorization)
    
    if payload["user_id"] == 1:
        return {"message": "List", "todos": todos}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

@app.post("/todos")
def create_todo(todo: Todo, authorization: str = Header(None)):
    payload = verify_token(authorization)
    
    if payload["user_id"] == 1:
        todos.append(todo)
        return {"message": "Todo created"}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: dict, authorization: str = Header(None)):
    payload = verify_token(authorization)
    
    if payload["user_id"] != 1:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    for i in range(len(todos)):
        if todos[i].id == todo_id:
            todos[i].title = todo["title"]
            todos[i].description = todo["description"]
            return {"message": "Todo updated"}
    
    raise HTTPException(status_code=404, detail="Todo not found")
    

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, authorization: str = Header(None)):
    payload = verify_token(authorization)
    
    if payload["user_id"] != 1:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": "Todo deleted"}
    
    raise HTTPException(status_code=404, detail="Todo not found")