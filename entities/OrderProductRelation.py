# library imports
from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel

class OrderProductRelation(SQLModel, table=True):
    __tablename__ = 'order_product_relations'
    id: int = Field(default=None, primary_key=True)
    orderId: int = Field(default=None, index=True)
    productId: int = Field(default=None, index=True)
    quantity: int

    __table_args__ = (
        ForeignKeyConstraint(["orderId"], ["orders.id"], name="order_product_relations_orderId_fkey", ondelete="CASCADE"),
        ForeignKeyConstraint(["productId"], ["products.id"], name="order_product_relations_ProductId_fkey", ondelete="CASCADE"),
    )
    
class OrderProductRelationUpdate(SQLModel):
    productId : int
    quantity: int
    