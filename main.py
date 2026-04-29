from fastapi import FastAPI
from routes import auth, tasks

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def home():
    return {"message": "HELLO"}