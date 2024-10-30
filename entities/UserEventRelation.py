# library imports
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int = Field(default=None, primary_key=True)
    userId: int
    eventId: int
    