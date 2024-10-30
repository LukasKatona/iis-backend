import datetime
from sqlmodel import Field, SQLModel

from enums.OrderStatus import OrderStatus

class Order(SQLModel, table=True):
    __tablename__ = 'orders'
    id: int = Field(default=None, primary_key=True)
    orderNumber: str
    userId: int = Field(default=None, foreign_key="users.id", index=True)
    farmerId: int = Field(default=None, foreign_key="farmers.id", index=True)
    reviewId: int = Field(default=None, foreign_key="reviews.id", nullable=True)
    status: OrderStatus = Field(default=OrderStatus.IN_CART)
    createdAt: datetime
    updatedAt: datetime = Field(nullable=True)
    suppliedAt: datetime = Field(nullable=True)
    