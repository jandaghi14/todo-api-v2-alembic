from pydantic import BaseModel, model_validator
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
    
    @model_validator(mode='after')
    def check_completed(self):
        if self.completed is True and self.priority is not None:
            raise ValueError("Cannot change priority of a completed todo")
        return self
            
    
class TodoShow(TodoCreate):
    id : int
    completed : bool
    created_at :datetime
    class Config:
        from_attributes = True



