# library imports
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from pydantic import BaseModel

# local imports
from enums.Unit import Unit

Base = declarative_base()

# Models for Pydanitc

class ProductModel(BaseModel):
    name: str
    imageUrl: str
    unit: Unit
    unitPrice: float
    stock: int
    categoryId: int

    class Config:
        from_attributes = True

class ProductCategoryModel(BaseModel):
    name: str
    parentCategoryId: int | None = None

    class Config:
        from_attributes = True

# Models for SQLAlchemy

class ProductORM(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    imageUrl: Mapped[str]
    unit: Mapped[Unit]
    unitPrice: Mapped[float]
    stock: Mapped[int]
    categoryId: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("product_categories.id"), index=True)

    def create_model(self) -> ProductModel:
        return ProductModel(
            name=self.name,
            imageUrl=self.imageUrl,
            unit=self.unit,
            unitPrice=self.unitPrice,
            stock=self.stock,
            categoryId=self.categoryId)

class ProductCategoryORM(Base):
    __tablename__ = 'product_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parentCategoryId: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("product_categories.id"), nullable=True)
    parentCategory: Mapped["ProductCategoryORM"] = relationship("ProductCategoryORM", back_populates="childCategories", remote_side="ProductCategoryORM.id")
    childCategories: Mapped[list["ProductCategoryORM"]] = relationship("ProductCategoryORM", back_populates="parentCategory")

    def create_model(self) -> ProductCategoryModel:
        return ProductCategoryModel(
            name=self.name,
            parentCategoryId=self.parentCategoryId)

ProductORM.category = relationship("ProductCategoryORM", back_populates="products")
ProductCategoryORM.products = relationship("ProductORM", back_populates="category")
