# library imports
from typing import Optional
import sqlalchemy as sa
from pydantic import BaseModel
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

class ProductCategory(SQLModel, table=True):
    __tablename__ = 'product_categories'
    id: int = Field(default=None, primary_key=True)
    name: str
    parentCategoryId: int = Field(default=None, foreign_key="product_categories.id", nullable=True)

    parentCategory: Optional["ProductCategory"] = Relationship(back_populates="childCategories", sa_relationship_kwargs={"remote_side": "ProductCategory.id"})
    childCategories: list["ProductCategory"] = Relationship(back_populates="parentCategory")

# relationships

Product.category = Relationship(back_populates="products")
ProductCategory.products = Relationship(back_populates="category")
