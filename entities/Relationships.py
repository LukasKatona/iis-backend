
from sqlmodel import Relationship

from entities.Product import Product
from entities.ProductCategory import ProductCategory
from entities.Order import Order

Product.category = Relationship(back_populates="products")
ProductCategory.products = Relationship(back_populates="category")
Order.products = Relationship(back_populates="orders")