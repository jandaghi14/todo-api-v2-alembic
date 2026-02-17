# Todo API v2

A clean REST API for managing todos, built with FastAPI, SQLAlchemy, and Alembic migrations.

## Features

- Full CRUD operations for todos
- SQLAlchemy ORM with SQLite
- Alembic database migrations
- Pydantic validation
- Dependency injection
- 9 comprehensive tests with test database isolation

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic
- pytest

## Project Structure
```
├── DataAccess/
│   ├── database.py
│   └── models.py
├── Business/
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

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/todo/` | Create a todo |
| GET | `/todo` | Get all todos |
| GET | `/todo/{id}` | Get a specific todo |
| PUT | `/todo/{id}` | Update a todo |
| DELETE | `/todo/{id}` | Delete a todo |

## Tests

Run tests:
```bash
pytest -v
```

9/9 tests passing with 100% endpoint coverage.