from fastapi import FastAPI,Depends,HTTPException
from Business.schemas import TodoBase, TodoCreate, TodoShow, TodoUpdate
from DataAccess.database import get_db,Base,engine
from sqlalchemy.orm import Session
from Business.crud import create_todo, get_all_todos, get_todo, update_todo, delete_todo
from DataAccess import models

app = FastAPI()

# Base.metadata.create_all(bind=engine)

@app.post('/todo/',response_model= TodoShow)
def endpoint_create_todo(todo:TodoCreate,db:Session=Depends(get_db)):
    return create_todo(todo, db)

@app.get('/todo',response_model= list[TodoShow])
def endpoint_get_all(db:Session=Depends(get_db)):

    result =  get_all_todos(db)
    if result :
        return result
    raise HTTPException(status_code=404, detail='No such todo')

@app.get('/todo/{todo_id}',response_model= TodoShow)
def endpoint_get_todo(todo_id:int,db:Session=Depends(get_db)):
    result = get_todo(todo_id, db)
    if result:
        return result
    raise HTTPException(status_code=404, detail='No such todo')

@app.put('/todo/{todo_id}',response_model= TodoShow)
def endpoint_update(todo_id:int, new_todo:TodoUpdate ,db:Session=Depends(get_db)):
    result =  update_todo(todo_id, new_todo,db)
    if result:
        return result
    raise HTTPException(status_code=404, detail='No such todo')

@app.delete('/todo/{todo_id}',response_model= str)
def endpoint_delete(todo_id:int, db:Session=Depends(get_db)):
    result =  delete_todo(todo_id, db)
    if result:
        return result
    raise HTTPException(status_code=404, detail='No such todo')