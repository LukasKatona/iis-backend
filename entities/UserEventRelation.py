# library imports
from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel

class UserEventRelation(SQLModel, table=True):
    __tablename__ = 'user_event_relations'
    id: int = Field(default=None, primary_key=True)
    userId: int = Field(default=None, index=True)
    eventId: int = Field(default=None, index=True)

    __table_args__ = (
        ForeignKeyConstraint(["userId"], ["users.id"], name="user_event_relations_userId_fkey"),
        ForeignKeyConstraint(["eventId"], ["events.id"], name="user_event_relations_eventId_fkey"),
    )
    