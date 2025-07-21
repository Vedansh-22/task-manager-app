from pydantic import BaseModel, EmailStr


class Task(BaseModel):
    taskName: str
    isCompleted: bool = False

class User(BaseModel):
    email: EmailStr
    password: str