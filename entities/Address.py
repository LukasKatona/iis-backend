# library imports
from sqlmodel import Field, SQLModel

class Address(SQLModel, table=True):
    __tablename__ = 'addresses'
    id: int = Field(default=None, primary_key=True)
    state: str = Field(nullable=True)
    city: str = Field(nullable=True)
    street: str = Field(nullable=True)
    streetNumber: str = Field(nullable=True)
    zipCode: str = Field(nullable=True)
    