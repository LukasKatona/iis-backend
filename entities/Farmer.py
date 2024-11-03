# library imports
from sqlalchemy import ForeignKeyConstraint
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
    )

    