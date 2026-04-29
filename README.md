# Task Manager API 🚀

## 📌 Overview

A backend application built using FastAPI that allows users to register, login, and manage tasks securely using JWT authentication.

## ⚙️ Features

* User Registration & Login
* Password Hashing (SHA256)
* JWT Authentication
* Task Management (CRUD)

  * Add Task
  * View Tasks
  * Update Task
  * Complete Task
  * Delete Task

---

## 🛠 Tech Stack

* Python
* FastAPI
* SQLite
* JWT (python-jose)

---

## 🚀 Run Locally

Install dependencies:

```
pip install -r requirements.txt
```

Run server:

```
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

1. Login to get token
2. Click 🔒 Authorize in Swagger
3. Enter:

```
Bearer <your_token>
```

---

## 📂 Project Structure

```
main.py
database.py
models.py
routes/
    auth.py
    tasks.py
```

---

## 👨‍💻 Author

Vasanth Kumar

