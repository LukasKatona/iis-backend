from sqlmodel import Field, SQLModel
import datetime

class Review(SQLModel, table=True):
    __tablename__ = 'reviews'
    id: int = Field(default=None, primary_key=True)
    userId: int = Field(foreign_key="users.id", index=True)
    productId: int = Field(foreign_key="products.id", index=True)
    rating: int
    review: str = Field(nullable=True)
    createdAt: datetime
    updatedAt: datetime = Field(nullable=True)
    deletedAt: datetime = Field(nullable=True)