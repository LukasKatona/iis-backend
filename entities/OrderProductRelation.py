# library imports
from sqlmodel import Field, SQLModel

class OrderProductRelation(SQLModel, table=True):
    __tablename__ = 'order_product_relations'
    id: int = Field(default=None, primary_key=True)
    orderId: int = Field(default=None, foreign_key="orders.id", index=True)
    ProductId: int = Field(default=None, foreign_key="products.id", index=True)
    quantity: int
    