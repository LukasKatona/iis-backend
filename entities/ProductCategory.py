# library imports
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class ProductCategory(SQLModel, table=True):
    __tablename__ = 'product_categories'
    id: int = Field(default=None, primary_key=True)
    name: str
    parentCategoryId: int = Field(default=None, foreign_key="product_categories.id", nullable=True)
    atributes: str = Field(default=None, nullable=True)

    parentCategory: Optional["ProductCategory"] = Relationship(back_populates="childCategories", sa_relationship_kwargs={"remote_side": "ProductCategory.id"})
    childCategories: list["ProductCategory"] = Relationship(back_populates="parentCategory")

class ProductCategoryUpdate(SQLModel):
    name: str