import datetime
from sqlmodel import Field, SQLModel

from enums.OrderStatus import OrderStatus

class Order(SQLModel, table=True):
    __tablename__ = 'orders'
    id: int = Field(default=None, primary_key=True)
    userId: int = Field(foreign_key="users.id", index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    totalPrice: float
    createdAt: datetime
    # updatedAt: datetime
    acceptedAt: datetime = Field(nullable=True)
    
