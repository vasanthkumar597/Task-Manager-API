from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    title: str