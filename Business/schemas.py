from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoBase(BaseModel):
    title : str
    description : str
    priority : int

class TodoCreate(TodoBase):
    pass
    
class TodoUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str]=None
    priority : Optional[int]=None
    completed :  Optional[bool]=None
    
class TodoShow(TodoCreate):
    id : int
    completed : bool
    created_at :datetime
    class Config:
        from_attributes = True



