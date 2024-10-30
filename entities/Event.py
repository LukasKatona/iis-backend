# library imports
from sqlmodel import Field, SQLModel

class Event(SQLModel, table=True):
    __tablename__ = 'events'
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    startDate: str
    endDate: str
    location: str
    createdById: int
    createdAt: str
    