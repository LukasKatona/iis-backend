from sqlmodel import Field, SQLModel
import datetime

class Review(SQLModel, table=True):
    __tablename__ = 'reviews'
    id: int = Field(default=None, primary_key=True)
    userId: int = Field(default=None, foreign_key="users.id", index=True)
    productId: int = Field(default=None, foreign_key="products.id", index=True, nullable=True)
    orderId: int = Field(default=None, foreign_key="orders.id", index=True, nullable=True)
    rating: int
    review: str = Field(nullable=True)
    createdAt: datetime