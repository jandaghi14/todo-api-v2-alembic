from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

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

def check_available_user(username:str,db:Session):
    from DataAccess.models import User
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    return None

def save_new_user(username, password, db:Session):
    from DataAccess.models import User
    user = User(username = username, hashed_password = password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    