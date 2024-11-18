# library imports
from typing import Optional
from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int = Field(default=None, primary_key=True)
    farmerId: int = Field(default=None, nullable=True)
    isAdmin: bool = Field(default=False)
    isModerator: bool = Field(default=False)
    isFarmer: bool = Field(default=False)
    isActive: bool = Field(default=True)

    name: str
    surname: str
    email: str
    password: str
    phone: str = Field(nullable=True)
    imageUrl: str = Field(nullable=True)
    
    state: str = Field(nullable=True)
    city: str = Field(nullable=True)
    street: str = Field(nullable=True)
    streetNumber: str = Field(nullable=True)
    zipCode: str = Field(nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["farmerId"], ["farmers.id"], name="users_farmerId_fkey", ondelete="SET NULL"),
    )

class UserUpdate(SQLModel):
    farmerId: Optional[int] = None
    isAdmin: Optional[bool] = None
    isModerator: Optional[bool] = None
    isFarmer: Optional[bool] = None
    isActive: Optional[bool] = None

    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    imageUrl: Optional[str] = None

    state: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    streetNumber: Optional[str] = None
    zipCode: Optional[str] = None
    