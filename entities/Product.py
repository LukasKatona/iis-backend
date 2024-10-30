# library imports
from sqlalchemy import ForeignKeyConstraint
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
    categoryId : int = Field(default=None, index=True, nullable=True)
    farmerId: int = Field(default=None, index=True)

    __table_args__ = (
        ForeignKeyConstraint(["categoryId"], ["product_categories.id"], name="products_categoryId_fkey"),
        ForeignKeyConstraint(["farmerId"], ["farmers.id"], name="products_farmerId_fkey"),
    )