
from sqlmodel import Relationship

from entities.Product import Product
from entities.ProductCategory import ProductCategory
from entities.User import User
from entities.UserEventRelation import UserEventRelation
from entities.Event import Event
from entities.Farmer import Farmer
from entities.Order import Order

# Product N -- 1 Category
Product.category = Relationship(back_populates="products")
ProductCategory.products = Relationship(back_populates="category")

# User 1 -- 1 Farmer
User.farmer = Relationship(back_populates="user")
Farmer.user = Relationship(back_populates="farmer")

# User N -- M Event
User.events = Relationship(UserEventRelation, back_populates="user")
UserEventRelation.user = Relationship(back_populates="events")
UserEventRelation.event = Relationship(back_populates="users")
Event.users = Relationship(UserEventRelation, back_populates="event")

# Farmer 1 -- N Event
Farmer.events = Relationship(Event, back_populates="createdByFarmer")
Event.farmer = Relationship(Farmer, back_populates="createdEvents")

# Farmer 1 -- N Product
Farmer.products = Relationship(Product, back_populates="farmer")
Product.farmer = Relationship(Farmer, back_populates="products")

Order.products = Relationship(back_populates="orders")