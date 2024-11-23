from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlmodel import Field, SQLModel

class Review(SQLModel, table=True):
    __tablename__ = 'reviews'
    id: int = Field(default=None, primary_key=True)
    userId: int = Field(default=None, index=True)
    productId: int = Field(default=None, index=True, nullable=True)
    orderId: int = Field(default=None, index=True, nullable=True)
    rating: int
    createdAt: float

    __table_args__ = (
        ForeignKeyConstraint(["userId"], ["users.id"], name="reviews_userId_fkey", ondelete="CASCADE"),
        ForeignKeyConstraint(["productId"], ["products.id"], name="reviews_productId_fkey", ondelete="CASCADE"),
        ForeignKeyConstraint(["orderId"], ["orders.id"], name="reviews_orderId_fkey", ondelete="CASCADE"),

        UniqueConstraint("userId", "productId", "orderId", name="reviews_userId_productId_orderId_key")
    )