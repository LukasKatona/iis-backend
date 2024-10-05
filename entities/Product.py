import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from enums.Unit import Unit

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    imageUrl: Mapped[str]
    unit: Mapped[Unit]
    unitPrice: Mapped[float]
    stock: Mapped[int]
    categoryId: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("product_categories.id"), index=True)

class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parentCategoryId: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("product_categories.id"), nullable=True)
    parentCategory: Mapped["ProductCategory"] = relationship("ProductCategory", back_populates="childCategories", remote_side="ProductCategory.id")
    childCategories: Mapped[list["ProductCategory"]] = relationship("ProductCategory", back_populates="parentCategory")

Product.category = relationship("ProductCategory", back_populates="products")
ProductCategory.products = relationship("Product", back_populates="category")
