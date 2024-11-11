# library imports
from typing import Optional
from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel

class Event(SQLModel, table=True):
    __tablename__ = 'events'
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    startDate: float
    endDate: float
    createdById: int = Field(default=None, index=True)
    createdAt: float

    state: str = Field(nullable=True)
    city: str = Field(nullable=True)
    street: str = Field(nullable=True)
    streetNumber: str = Field(nullable=True)
    zipCode: str = Field(nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["createdById"], ["farmers.id"], name="events_createdById_fkey", ondelete="CASCADE"),
    )

class EventUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    startDate: Optional[float] = None
    endDate: Optional[float] = None

    state: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    streetNumber: Optional[str] = None
    zipCode: Optional[str] = None