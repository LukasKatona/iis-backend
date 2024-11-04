# library imports
from typing import Optional
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlmodel import Field, SQLModel

class Farmer(SQLModel, table=True):
    __tablename__ = 'farmers'
    id: int = Field(default=None, primary_key=True)
    userId: int = Field(default=None)
    farmName: str = Field(nullable=True)
    description: str = Field(nullable=True)

    CIN: str # Company Identification Number (ICO)
    VATIN: str # Value Added Tax Identification Number (DIC)
    VAT: str # Value Added Tax (IC DPH)
    paysVat: bool = Field(default=False)

    bankCode: str
    accountNumber: str
    iban: str = Field(nullable=True)

    state: str = Field(nullable=True)
    city: str = Field(nullable=True)
    street: str = Field(nullable=True)
    streetNumber: str = Field(nullable=True)
    zipCode: str = Field(nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["userId"], ["users.id"], name="farmers_userId_fkey", ondelete="CASCADE"),
        UniqueConstraint("userId", name="unique_user_per_farmer"),
    )

class FarmerUpdate(SQLModel):
    farmName: Optional[str] = None
    description: Optional[str] = None

    CIN: Optional[str] = None
    VATIN: Optional[str] = None
    VAT: Optional[str] = None
    paysVat: Optional[bool] = None

    bankCode: Optional[str] = None
    accountNumber: Optional[str] = None
    iban: Optional[str] = None

    state: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    streetNumber: Optional[str] = None
    zipCode: Optional[str] = None