# library imports
from sqlmodel import Field, SQLModel, Relationship

# local imports
from enums.Unit import Unit

class Product(SQLModel, table=True):
    __tablename__ = 'products'
    id: int = Field(default=None, primary_key=True)
    name: str
    imageUrl: str
    unit: Unit
    unitPrice: float
    stock: int
    categoryId : int = Field(default=None, foreign_key="product_categories.id", index=True, nullable=True)