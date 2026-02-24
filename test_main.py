from fastapi.testclient import TestClient
from fastapi import Depends
import pytest
from DataAccess.database import get_db
from Business.schemas import TodoCreate,TodoShow,TodoUpdate
from Business.crud import create_todo
import os
from DataAccess.database import Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from sqlalchemy.orm import Session
import time

DB_test = 'sqlite:///./test_db.db'
engine = create_engine(DB_test, connect_args={'check_same_thread': False})
session_test = sessionmaker(bind=engine, autoflush=False, autocommit= False)

def override_get_db():
    db = session_test()
    yield db
    db.close()

@pytest.fixture
def set_up_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(set_up_db):
    return TestClient(app)

@pytest.fixture
def auth_header(client):
    client.post('/register', params={'username':'testuser', 'password':'testpass'})
    response = client.post('/login', data={'username':'testuser', 'password':'testpass'})

    token = response.json()['access_token']
    return {'Authorizations': f'Bearer {token}'} 



def test_create_todo(client, auth_header):
    response= client.post('/todo/',json={'title':'test_title',
                                      'description' : 'test_desctiption',
                                      'priority': 1
                                      },headers=auth_header )
    assert response.status_code == 200
    assert response.json()['title'] == 'test_title'
    # ===============================
def test_get_all_todos(client, auth_header):
    client.post('/todo/',json={'title':'test_title1',
                                      'description' : 'test_desctiption1',
                                      'priority': 1
                                      },headers=auth_header )
    client.post('/todo/',json={'title':'test_title2',
                                      'description' : 'test_desctiption2',
                                      'priority': 2
                                      } ,headers=auth_header)

    response= client.get('/todo',headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) == 2
    # ===============================
def test_get_todos(client, auth_header):
    client.post('/todo/',json={'title':'test_title1',
                                      'description' : 'test_desctiption1',
                                      'priority': 1
                                      } ,headers=auth_header)
    client.post('/todo/',json={'title':'test_title2',
                                      'description' : 'test_desctiption2',
                                      'priority': 2
                                      } ,headers=auth_header)

    response= client.get('/todo/2',headers=auth_header)
    assert response.status_code == 200
    assert response.json()['title'] == 'test_title2'
    # ===============================
def test_get_todos_fail(client, auth_header):
    response= client.get('/todo/2',headers=auth_header)
    assert response.status_code == 404
    assert response.json()['detail'] == 'No such todo'

    # ===============================

def test_update_todo(client, auth_header):
    client.post('/todo/',json={'title':'test_title',
                                      'description' : 'test_desctiption',
                                      'priority': 1
                                      },headers=auth_header )
    response= client.put('/todo/1', json={'title':'update',
                                      'description' : 'update_desc',
                                      'priority': 1,
                                      'completed': False
    },headers=auth_header)

    assert response.status_code == 200
    assert response.json()['title'] == 'update'
    assert response.json()['description'] == 'update_desc'
    assert response.json()['priority'] == 1
    assert response.json()['completed'] == False
    # ===============================
def test_update_todo_fail(client, auth_header):
    response= client.put('/todo/1', json={'title':'update',
                                      'description' : 'update_desc',
                                      'priority': 2,
                                      'completed': False
    },headers=auth_header)

    assert response.status_code == 404
    assert response.json()['detail'] == 'No such todo'
    # ===============================
def test_update_completed(client, auth_header):
    client.post('/todo/',json={'title':'test_title',
                                      'description' : 'test_desctiption',
                                      'priority': 1
                                      } ,headers=auth_header)
    response= client.put('/todo/1', json={'title':'update',
                                      'description' : 'update_desc',
                                      'priority': 2,
                                      'completed': True
    },headers=auth_header)
    assert response.status_code == 422

def test_delete_todo(client, auth_header):
    client.post('/todo/',json={'title':'test_title',
                                      'description' : 'test_desctiption',
                                      'priority': 1
                                      } ,headers=auth_header)
    response = client.delete('/todo/1',headers=auth_header)
    assert response.status_code == 200
    assert response.json() == 'Deletion successfully'
    # ===============================
def test_delete_todo_fail(client, auth_header):
    response = client.delete('/todo/1',headers=auth_header)
    assert response.status_code == 404
    assert response.json()['detail'] == 'No such todo'


