import os
from datetime import datetime, timedelta

from fastapi.params import Depends
from jose import jwt
from fastapi import FastAPI, HTTPException
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from auth.utils import encrypt_password, get_current_user, verify_password, user_table, task_table, SECRET_KEY
from auth.utils import ALGORITHM
from models import Task, User

load_dotenv()
app = FastAPI()

@app.post("/register")
def register_user(user: User):
    isExisting = user_table.find_one({"email": user.email})
    if isExisting:
        return {"message": "User already exists"}
    password = user.password
    hashed_pass = encrypt_password(password)
    prepared_user = {
        "email": user.email,
        "password": hashed_pass.decode("utf-8")
    }
    res = user_table.insert_one(prepared_user)
    if res:
        return {"message": "User registered successfully"}
    return {"message": "User registration failed"}

@app.post("/login")
def login_user(user: User):
    password = user.password
    hashed_pass = encrypt_password(password)
    is_verified = verify_password(password, hashed_pass)
    if not is_verified:
        return {"message": "User login failed, Incorrect Username or Password"}

    payload = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    jwt_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return jwt_token


@app.get("/tasks")
def get_tasks(current_user: dict = Depends(get_current_user)):
    cursor = task_table.find({"user_id":current_user["_id"]})
    return [{"id": str(task["_id"]),"taskName": task['taskName'], "isCompleted": task['isCompleted']} for task in cursor]

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: str):
    cursor = task_table.find_one({"_id": ObjectId(task_id)})
    if not cursor:
        raise HTTPException(status_code=404, detail=f"NO Task Found for ID : {task_id}")
    return [{"id": str(cursor["_id"]),"taskName": cursor['taskName'], "isCompleted": cursor['isCompleted']}]

@app.post("/task")
def create_task(task:Task, current_user:dict=Depends(get_current_user)):
    task_to_add = {
        "user_id": current_user["_id"],
        "taskName": task.taskName,
        "isCompleted": task.isCompleted,
    }
    res = task_table.insert_one(task_to_add)
    if res.inserted_id:
        return {"message": "Task created successfully", "task_id": str(res.inserted_id)}
    return {"message": "Task could not be created"}

@app.put("/tasks/{task_id}")
async def update_task(task_id:str, task : Task, current_user :dict=Depends(get_current_user)):
    print(f"received task : {task}")
    find_id = ObjectId(task_id)
    found_task = task_table.find_one({"_id": find_id,"user_id":current_user["_id"]})
    print(f"found_task ::: {found_task}")
    if found_task:
        updated_payload={
            "user_id":current_user["_id"],
            "taskName": task.taskName,
            "isCompleted": task.isCompleted
        }
        res = task_table.update_one({"_id": find_id}, {"$set": updated_payload})
        if res.modified_count>0:
            updated_task = task_table.find_one({"_id": find_id})
            return {
                "id": str(updated_task["_id"]),
                "taskName": updated_task['taskName'],
                "isCompleted": updated_task['isCompleted']
            }
        else:
            raise HTTPException(status_code=400, detail="Task not modified")
    raise HTTPException(status_code=402, detail=f"task not found for id {task_id}")


@app.delete("/tasks/{task_id}")
def delete_task(task_id:str, current_user:dict=Depends(get_current_user)):
    resp = task_table.delete_one({"_id": ObjectId(task_id), "user_id":current_user["_id"]})
    if resp.deleted_count==0:
        raise HTTPException(status_code=404, detail="Task not found")
    return f"task {task_id} deleted successfully"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], )
