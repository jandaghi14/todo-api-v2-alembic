from fastapi import FastAPI,Depends,HTTPException
from Business.schemas import TodoBase, TodoCreate, TodoShow, TodoUpdate
from DataAccess.database import get_db,Base,engine
from sqlalchemy.orm import Session
from Business.crud import create_todo, get_all_todos, get_todo, update_todo, delete_todo
from DataAccess import models
from Business.auth_routes import router as auth_router
from Business.auth import get_current_user

from fastapi.middleware.cors import CORSMiddleware
from time import time

# Frontend origins that can access your backend
origins = [
    "http://localhost:3000",   # React development server
    "http://127.0.0.1:3000",   # sometimes used interchangeably
]


app = FastAPI()
# Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True)

app.include_router(auth_router)

@app.middleware("http") # this tells FastAPI: run this function for every HTTP request before it reaches any endpoint.
async def log_requests(request, call_next):
    # request — the incoming request object (method, path, headers, etc.)
    # call_next — a function that forwards the request to the actual endpoint
    # --- BEFORE endpoint ---
    start = time()
    print(f"Incoming: {request.method} {request.url.path}")
    # --- endpoint runs here ---
    response = await call_next(request) #This says: "pass the request to the actual endpoint now, wait for it to finish, and give me back the response."
    # --- AFTER endpoint ---
    duration = time() - start
    print(f"Completed: {response.status_code} in {duration:.3f}s")
    
    return response





@app.post('/todo/',response_model= TodoShow)
def endpoint_create_todo(todo:TodoCreate,current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):
    return create_todo(todo, db)

@app.get('/todo',response_model= list[TodoShow])
def endpoint_get_all(current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):

    result =  get_all_todos(db)
    if result :
        return result
    raise HTTPException(status_code=404, detail='No such todo')

@app.get('/todo/{todo_id}',response_model= TodoShow)
def endpoint_get_todo(todo_id:int,current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):
    result = get_todo(todo_id, db)
    if result:
        return result
    raise HTTPException(status_code=404, detail='No such todo')

@app.put('/todo/{todo_id}',response_model= TodoShow)
def endpoint_update(todo_id:int, new_todo:TodoUpdate,current_user:str=Depends(get_current_user) ,db:Session=Depends(get_db)):
    result =  update_todo(todo_id, new_todo,db)
    if result:
        return result
    raise HTTPException(status_code=404, detail='No such todo')

@app.delete('/todo/{todo_id}',response_model= str)
def endpoint_delete(todo_id:int,current_user:str=Depends(get_current_user), db:Session=Depends(get_db)):
    result =  delete_todo(todo_id, db)
    if result:
        return result
    raise HTTPException(status_code=404, detail='No such todo')



