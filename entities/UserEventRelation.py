# library imports
from sqlmodel import Field, SQLModel

class UserEventRelation(SQLModel, table=True):
    __tablename__ = 'user_event_relations'
    id: int = Field(default=None, primary_key=True)
    userId: int
    eventId: int
    