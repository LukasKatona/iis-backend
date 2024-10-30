# library imports
from sqlmodel import Field, SQLModel

class UserEventRelation(SQLModel, table=True):
    __tablename__ = 'user_event_relations'
    id: int = Field(default=None, primary_key=True)
    userId: int = Field(default=None, foreign_key="users.id", index=True)
    eventId: int = Field(default=None, foreign_key="events.id", index=True)
    