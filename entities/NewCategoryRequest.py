from sqlmodel import Field, SQLModel

from enums.CategoryRequestState import CategoryRequestState

class NewCategoryRequest(SQLModel, table=True):
    __tablename__ = 'new_category_requests'
    newCategoryName: str
    state = Field(default=CategoryRequestState.PENDING)
    parentCategoryId: int = Field(default=None, foreign_key="product_categories.id", nullable=True)
    createdById: int = Field(default=None, foreign_key="users.id", index=True)
