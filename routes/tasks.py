from fastapi import APIRouter, Header
from models import Task
from database import cursor, conn
from .auth import verify_token
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security=HTTPBearer()

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/add-task")
def add_task(task: Task, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username=verify_token(token)

    if not username:
        return {"status": "error", "message": "invalid token"}
    

    cursor.execute("INSERT INTO tasks (username,title,completed) VALUES (?,?,?)",
                   (username,task.title,0)
                   )
    conn.commit()
    return {"status": "success", "message": "task added"}

@router.put("/update-task/{task_id}")
def update_task(
    task_id: int,
    task: Task,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        return {"status": "error", "message": "invalid token"}
    
    cursor.execute("SELECT * FROM tasks WHERE id=? AND username=?",(task_id,username))
    if not cursor.fetchone():
        return{"status": "error", "message":"task not found or not yours"}
    
    cursor.execute("UPDATE tasks SET title=? WHERE id=?",
                   (task.title,task_id)
                   )
    conn.commit()
    return {"status": "success","message":"task updated"}

@router.put("/complete-task/{task_id}")
def complete_task(
    task_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    username = verify_token(token)


    if not username:
        return{"status": "error","message":"invalid token"}
    
    cursor.execute("SELECT * FROM tasks WHERE id=? AND username=?",(task_id,username))
    if not cursor.fetchone():
        return{"status": "error","message":"task not found or not yours"}
    
    

    cursor.execute(
    "UPDATE tasks SET completed=1 WHERE id=?",
    (task_id,)
    )
    conn.commit()
    return {"status": "success","message":"task completed"}

@router.delete("/delete-task/{task_id}")
def delete_task(
    task_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        return {"status": "error", "message": "invalid token"}
    cursor.execute("SELECT * FROM tasks WHERE id=? AND username=?",(task_id,username))
    if not cursor.fetchone():
        return{"status": "error", "message": "task not found"}
    
    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )
    conn.commit()
    return {"status": "success", "message": "task deleted"}



@router.get("/tasks")
def get_tasks(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    username = verify_token(token)

    if not username:
        return{"status": "error", "message": "invalid token"}
    
    cursor.execute("SELECT * FROM tasks WHERE username=?",(username,))
    tasks=cursor.fetchall()
    return {"status": "success", "data": tasks}