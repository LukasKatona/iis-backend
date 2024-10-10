
from sqlmodel import Relationship

from entities.Product import Product
from entities.ProductCategory import ProductCategory

Product.category = Relationship(back_populates="products")
ProductCategory.products = Relationship(back_populates="category")