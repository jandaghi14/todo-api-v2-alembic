from fastapi import APIRouter, HTTPException, Depends
from DataAccess.database import check_available_user, save_new_user
from sqlalchemy.orm import Session
from Business import auth
from DataAccess.database import get_db



router = APIRouter()

@router.post('/register')
def endpoint_register(username:str, password:str, db:Session= Depends(get_db)):
    user = check_available_user(username,db)
    if user:
        raise HTTPException(status_code=404, detail='Username already taken')
    hashed_pass = auth.hash_password(password)
    save_new_user(username,hashed_pass,db)
    return 'success'

from fastapi.security import OAuth2PasswordRequestForm

@router.post('/login')
def endpoint_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = check_available_user(form_data.username, db)
    if not user:
        raise HTTPException(status_code=404, detail='Username does not exist')
    if auth.verify_password(form_data.password, user.hashed_password):
        return {"access_token": auth.create_access_token(form_data.username), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Wrong password")