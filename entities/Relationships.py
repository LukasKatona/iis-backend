
from sqlmodel import Relationship

from entities.Address import Address
from entities.Product import Product
from entities.ProductCategory import ProductCategory
from entities.User import User
from entities.UserEventRelation import UserEventRelation
from entities.Event import Event
from entities.Farmer import Farmer
from entities.Order import Order
from entities.OrderProductRelation import OrderProductRelation
from entities.Review import Review
from entities.NewCategoryRequest import NewCategoryRequest

# Product N -- 1 Category
Product.category = Relationship(ProductCategory, back_populates="products")
ProductCategory.products = Relationship(Product, back_populates="category")

# User 1 -- 1 Farmer
User.farmer = Relationship(Farmer, back_populates="user")
Farmer.user = Relationship(User, back_populates="farmer")

# User N -- M Event
User.events = Relationship(UserEventRelation, back_populates="user")
UserEventRelation.user = Relationship(User, back_populates="events")
UserEventRelation.event = Relationship(Event, back_populates="users")
Event.users = Relationship(UserEventRelation, back_populates="event")

# Farmer 1 -- N Event
Farmer.createdEvents = Relationship(Event, back_populates="createdByFarmer")
Event.createdByFarmer = Relationship(Farmer, back_populates="createdEvents")

# Farmer 1 -- N Product
Farmer.products = Relationship(Product, back_populates="farmer")
Product.farmer = Relationship(Farmer, back_populates="products")

# Farmer 1 -- N Order
Farmer.incomingOrders = Relationship(Order, back_populates="farmer")
Order.farmer = Relationship(Farmer, back_populates="incomingOrders")

# User 1 -- N Order
User.outgoingOrders = Relationship(Order, back_populates="user")
Order.user = Relationship(User, back_populates="outgoingOrders")

# Order N -- M Product
Order.products = Relationship(OrderProductRelation, back_populates="order")
OrderProductRelation.order = Relationship(Order, back_populates="products")
OrderProductRelation.product = Relationship(Product, back_populates="orders")
Product.orders = Relationship(OrderProductRelation, back_populates="product")

# User 1 -- N Review
User.reviews = Relationship(Review, back_populates="user")
Review.user = Relationship(User, back_populates="reviews")

# Product 1 -- N Review
Product.reviews = Relationship(Review, back_populates="product")
Review.product = Relationship(Product, back_populates="reviews")

# Order 1 -- N Review
Order.reviews = Relationship(Review, back_populates="order")
Review.order = Relationship(Order, back_populates="reviews")

# New Category Request N -- 1 Category
NewCategoryRequest.parentCategory = Relationship(ProductCategory, back_populates="newChildCategoryRequests")
ProductCategory.newChildCategoryRequests = Relationship(NewCategoryRequest, back_populates="parentCategory")

# New Category Request N -- 1 User
NewCategoryRequest.createdByUser = Relationship(User, back_populates="newCategoryRequests")
User.newCategoryRequests = Relationship(NewCategoryRequest, back_populates="createdByUser")

# Address 1 -- 1 Event
Event.address = Relationship(Address, back_populates="event")
Address.event = Relationship(Event, back_populates="address")

# Address 1 -- 1 Farmer
Farmer.address = Relationship(Address, back_populates="farmer")
Address.farmer = Relationship(Farmer, back_populates="address")

# Address 1 -- 1 User
User.address = Relationship(Address, back_populates="user")
Address.user = Relationship(User, back_populates="address")