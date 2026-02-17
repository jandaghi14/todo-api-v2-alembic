from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DB_Name= 'sqlite:///./todo_database.db'
engine= create_engine(DB_Name, connect_args = {'check_same_thread':False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit = False)
Base= declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()