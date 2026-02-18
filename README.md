# Todo API v2
A clean REST API for managing todos with JWT authentication, built with FastAPI, SQLAlchemy, and Alembic migrations.

## Features
- Full CRUD operations for todos
- JWT authentication (register, login, protected routes)
- Password hashing with bcrypt
- SQLAlchemy ORM with SQLite
- Alembic database migrations
- Pydantic validation with cross-field rules (completed todos cannot have priority changed)
- Dependency injection
- 9 comprehensive tests with test database isolation

## Tech Stack
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic
- python-jose (JWT)
- passlib (bcrypt)
- pytest

## Project Structure
```
├── DataAccess/
│   ├── database.py
│   └── models.py
├── Business/
│   ├── auth.py
│   ├── auth_routes.py
│   ├── crud.py
│   └── schemas.py
├── alembic/
│   └── versions/
├── main.py
├── test_main.py
└── requirements.txt
```

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Apply migrations:
```bash
alembic upgrade head
```
3. Run the server:
```bash
uvicorn main:app --reload
```
4. Open docs: `http://127.0.0.1:8000/docs`

## Authentication Flow
1. Register: `POST /register?username=your_name&password=your_pass`
2. Login: `POST /login` → returns JWT token
3. Use the Authorize button in docs to attach token to all requests

## API Endpoints
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/register` | No | Register a new user |
| POST | `/login` | No | Login and get JWT token |
| POST | `/todo/` | Yes | Create a todo |
| GET | `/todo` | Yes | Get all todos |
| GET | `/todo/{id}` | Yes | Get a specific todo |
| PUT | `/todo/{id}` | Yes | Update a todo |
| DELETE | `/todo/{id}` | Yes | Delete a todo |

## Example Request
```json
POST /todo/
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": 2
}
```

## Tests
Run tests:
```bash
pytest -v
```
9/9 tests passing with 100% endpoint coverage.