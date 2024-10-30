# library imports
from sqlmodel import Field, SQLModel

# local imports
from enums.Role import Role

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int = Field(default=None, primary_key=True)
    farmerId: int = Field(default=None, foreign_key="farmers.id", nullable=True)
    role: Role = Field(default=Role.GUEST)
    name: str
    surname: str
    email: str
    password: str
    phone: str = Field(nullable=True)
    imageUrl: str = Field(nullable=True)
    addressId: int = Field(default=None, foreign_key="addresses.id", nullable=True)
    