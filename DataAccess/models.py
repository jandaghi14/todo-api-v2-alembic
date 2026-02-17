from DataAccess.database import Base
from sqlalchemy import Integer,String, Column, DateTime, Boolean
from datetime import datetime, timezone


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer,autoincrement=True,primary_key=True,index=True )
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True, index=True)
    priority = Column(Integer, nullable=False,index=True)
    created_at = Column(DateTime, nullable=False, index=True, default= lambda: datetime.now(timezone.utc))
    completed = Column(Boolean, index= True, default=False,nullable=False)
    