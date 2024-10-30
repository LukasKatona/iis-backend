# library imports
from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel

# local imports
from enums.Role import Role

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int = Field(default=None, primary_key=True)
    farmerId: int = Field(default=None, nullable=True)
    role: Role = Field(default=Role.GUEST)
    name: str
    surname: str
    email: str
    password: str
    phone: str = Field(nullable=True)
    imageUrl: str = Field(nullable=True)
    addressId: int = Field(default=None, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["farmerId"], ["farmers.id"], name="users_farmerId_fkey"),
        ForeignKeyConstraint(["addressId"], ["addresses.id"], name="users_addressId_fkey"),
    )
    