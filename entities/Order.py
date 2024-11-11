from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel

from enums.OrderStatus import OrderStatus

class Order(SQLModel, table=True):
    __tablename__ = 'orders'
    id: int = Field(default=None, primary_key=True)
    orderNumber: str
    userId: int = Field(default=None, index=True, nullable=True)
    farmerId: int = Field(default=None, index=True, nullable=True)
    reviewId: int = Field(default=None, nullable=True)
    status: OrderStatus = Field(default=OrderStatus.IN_CART)
    createdAt: float
    updatedAt: float = Field(nullable=True)
    suppliedAt: float = Field(nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["userId"], ["users.id"], name="orders_userId_fkey", ondelete="SET NULL"),
        ForeignKeyConstraint(["farmerId"], ["farmers.id"], name="orders_farmerId_fkey", ondelete="SET NULL"),
        ForeignKeyConstraint(["reviewId"], ["reviews.id"], name="orders_reviewId_fkey", ondelete="SET NULL"),
    )


    