# library imports
from typing import Optional
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
    unitPrice: float = Field(default=0.0)
    VAT: float = Field(default=0.0)
    stock: int = Field(default=0)
    categoryId : int = Field(default=None, index=True, nullable=True)
    farmerId: int = Field(default=None, index=True)

    __table_args__ = (
        ForeignKeyConstraint(["categoryId"], ["product_categories.id"], name="products_categoryId_fkey", ondelete="SET NULL"),
        ForeignKeyConstraint(["farmerId"], ["farmers.id"], name="products_farmerId_fkey", ondelete="CASCADE"),
    )

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    imageUrl: Optional[str] = None
    unit: Optional[Unit] = None
    unitPrice: Optional[float] = None
    VAT: Optional[float] = None
    stock: Optional[int] = None
    categoryId: Optional[int] = None

class ProductWithQuantity(SQLModel):
    product: Product
    quantity: int