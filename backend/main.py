from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client.get_database("taskdb")
task_table = db.get_collection("tasks")


class Task(BaseModel):
    taskName: str
    isCompleted: bool = False

@app.get("/tasks")
def get_tasks():
    cursor = task_table.find()
    return [{"id": str(task["_id"]),"taskName": task['taskName'], "isCompleted": task['isCompleted']} for task in cursor]

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: str):
    cursor = task_table.find_one({"_id": ObjectId(task_id)})
    if not cursor:
        raise HTTPException(status_code=404, detail=f"NO Task Found for ID : {task_id}")
    return [{"id": str(cursor["_id"]),"taskName": cursor['taskName'], "isCompleted": cursor['isCompleted']}]

@app.post("/task")
def create_task(task:Task):
    task_to_add = {
        "taskName": task.taskName,
        "isCompleted": task.isCompleted,
    }
    res = task_table.insert_one(task_to_add)
    if res:
        return f"task {task_to_add} created successfully"
    return f"task {task_to_add} could not be created"

@app.put("/tasks/{task_id}")
async def update_task(task_id:str, task : Task):
    print(f"received task : {task}")
    find_id = ObjectId(task_id)
    found_task = task_table.find_one({"_id": find_id})
    if found_task:
        res = task_table.update_one({"_id": find_id}, {"$set": task.model_dump()})
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
def delete_task(task_id:str):
    resp = task_table.delete_one({"_id": ObjectId(task_id)})
    if resp.deleted_count==0:
        raise HTTPException(status_code=404, detail="Task not found")
    return f"task {task_id} deleted successfully"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], )
