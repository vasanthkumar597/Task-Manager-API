from fastapi import APIRouter,Header
from models import User
from database import cursor, conn
import hashlib
from jose import jwt

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"


def create_token(username: str):
    return jwt.encode({"username": username}, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    if not token:
        return None
    
    if token.startswith("Bearer "):
            token=token.split(" ")[1]
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data["username"]
    except:
        return None


@router.post("/register")
def register(user: User):

    cursor.execute("SELECT * FROM users WHERE username=?", (user.username,))
    if cursor.fetchone():
        return {"status": "error", "message": "user already exists"}

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user.username, hashed_password)
    )
    conn.commit()

    return {"status": "success", "message": "registration successful"}


@router.post("/login")
def login(user: User):

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user.username, hashed_password)
    )

    if not cursor.fetchone():
        return {"status": "error", "message": "invalid credentials"}

    token = create_token(user.username)

    return {
        "status": "success",
        "message": "login successful",
        "token": token
    }

@router.delete("/delete-user")
def delete_user(authorization: str = Header(None, alias="authorization")):

    username = verify_token(authorization)

    if not username:
        return {"status": "error", "message": "invalid token"}

    
    cursor.execute("DELETE FROM tasks WHERE username=?", (username,))

    
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    
    conn.commit()

    return {"status": "success", "message": "user deleted successfully"}

@router.get("/users")
def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()