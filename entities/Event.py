# library imports
from sqlmodel import Field, SQLModel

class Event(SQLModel, table=True):
    __tablename__ = 'events'
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    startDate: str
    endDate: str
    createdById: int = Field(default=None, foreign_key="farmers.id", index=True)
    createdAt: str

    addressId: int = Field(default=None, foreign_key="addresses.id")
    