import os
from http.client import HTTPException

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]

task_table = db["tasks"]
user_table = db["users"]


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


security = HTTPBearer()


def encrypt_password(password: str):
    salt =  bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pass

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get('sub')
        if user_email is None:
            raise HTTPException(status_code=401, details="Invalid Token: User ID not found")
        user_payload = user_table.find_one({"email":user_email})
        return user_payload
    except JWTError:
        raise HTTPException(status_code=401, details="Invalid Token")

