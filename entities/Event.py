# library imports
from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel

class Event(SQLModel, table=True):
    __tablename__ = 'events'
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    startDate: str
    endDate: str
    createdById: int = Field(default=None, index=True)
    createdAt: str

    addressId: int = Field(default=None)

    __table_args__ = (
        ForeignKeyConstraint(["createdById"], ["farmers.id"], name="events_createdById_fkey"),
        ForeignKeyConstraint(["addressId"], ["addresses.id"], name="events_addressId_fkey"),
    )