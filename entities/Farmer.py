# library imports
from sqlmodel import Field, SQLModel

class Farmer(SQLModel, table=True):
    __tablename__ = 'farmers'
    id: int = Field(default=None, primary_key=True)
    userId: int = Field(default=None, foreign_key="users.id")
    farmName: str = Field(nullable=True)
    description: str = Field(nullable=True)
    
    CIN: str # Company Identification Number (ICO)
    VATIN: str # Value Added Tax Identification Number (DIC)
    VAT: str # Value Added Tax (IC DPH)
    paysVat: bool

    bankCode: str
    accountNumber: str
    iban: str = Field(nullable=True)

    