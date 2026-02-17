from Business.schemas import  TodoCreate,  TodoUpdate
from sqlalchemy.orm import Session
from DataAccess.models import Todo

def create_todo(todo:TodoCreate,db:Session):
    db_todo = Todo(
        title = todo.title,
        description = todo.description,
        priority = todo.priority
        )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_all_todos(db:Session):
    todos = db.query(Todo).all()
    if todos:
        return todos
    return []
def get_todo(todo_id:int, db:Session):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        return todo
    return None
def update_todo(todo_id: int, new_todo:TodoUpdate , db:Session):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None
    if new_todo.title is not None:
        todo.title = new_todo.title
    if new_todo.description is not None:
        todo.description = new_todo.description
    if new_todo.priority is not None:
        todo.priority = new_todo.priority
    if new_todo.completed is not None:
        todo.completed = new_todo.completed
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(todo_id: int, db:Session):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return "Deletion successfully"
    