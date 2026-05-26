# Authentication_Authorization

# FastAPI Authentication & Authorization API

A FastAPI backend project with:

- JWT Authentication
- Role-Based Authorization
- PostgreSQL
- SQLAlchemy ORM
- Pagination
- Logging
- Clean Service Architecture

---

# Features

- User Registration
- User Login
- JWT Token Authentication
- Password Hashing using bcrypt
- Change Password
- Admin Protected Routes
- Pagination Support
- Transaction Management
- Exception Handling

---

# Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Pydantic

---

# Project Structure

```bash
AUTH_PROJECT/
│
├── app/
│   │
│   ├── core/
│   │   ├── auth.py
│   │   └── response.py
│   │
│   ├── models/
│   │   └── user_models.py
│   │
│   ├── repository/
│   │   └── user_repository.py
│   │
│   ├── routers/
│   │   └── user_router.py
│   │
│   ├── schemas/
│   │   └── user_schemas.py
│   │
│   ├── services/
│   │   └── user_service.py
│   │
│   ├── utils/
│   │   └── decorators.py
│   │
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── .env
├── .gitignore
├── LOG_FILE
├── README.md
└── requirements.txt
```

---

# Installation

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://username:password@host:5432/database_name

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Render PostgreSQL URL Setup

If you are using Render PostgreSQL Database:

Go to:

```text
Render Dashboard → PostgreSQL → Connections
```

Copy:

```text
External Database URL
```

Example:

```env
DATABASE_URL=postgresql://postgres:password@dpg-xxxx.render.com/database_name
```

Paste it inside `.env`

---

# Run Project

```bash
uvicorn main:app --reload
```

---

# Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

# Authentication

## Register

```http
POST /register
```

## Login

```http
POST /login
```

---

# Authorization

Protected routes require:

```text
Authorization: Bearer <token>
```

---

# Admin Routes

- `/all_users`
- `/users/{id}`
- `/create-admin`

---

# Pagination

```http
GET /all_users?skip=0&limit=10
```

---

# Requirements

```txt
fastapi
uvicorn[standard]

sqlalchemy
psycopg2-binary

python-jose[cryptography]

passlib[bcrypt]
bcrypt==4.0.1

pydantic
pydantic-settings
email-validator

python-dotenv
```

---

