from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel

from enums.CategoryRequestState import CategoryRequestState

class NewCategoryRequest(SQLModel, table=True):
    __tablename__ = 'new_category_requests'
    id: int = Field(default=None, primary_key=True)
    newCategoryName: str
    state: CategoryRequestState = Field(default=CategoryRequestState.PENDING)
    parentCategoryId: int = Field(default=None, nullable=True)
    createdById: int = Field(default=None, index=True, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["parentCategoryId"], ["product_categories.id"], name="newcategoryrequest_parentCategoryId_fkey", ondelete="CASCADE"),
        ForeignKeyConstraint(["createdById"], ["users.id"], name="newcategoryrequest_createdById_fkey", ondelete="SET NULL"),
    )