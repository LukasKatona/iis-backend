# library imports
from sqlmodel import Field, SQLModel

# local imports
from enums.Unit import Unit

class Product(SQLModel, table=True):
    __tablename__ = 'products'
    id: int = Field(default=None, primary_key=True)
    name: str
    imageUrl: str = Field(nullable=True)
    unit: Unit = Field(default=Unit.KILOGRAM)
    unitPrice: float
    VAT: float = Field(default=0.0)
    stock: int
    categoryId : int = Field(default=None, foreign_key="product_categories.id", index=True, nullable=True)
    farmerId: int = Field(nullable=True)