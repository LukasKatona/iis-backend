from sqlmodel import Field, SQLModel

from enums.CategoryRequestState import Category

class NewCategoryRequest(SQLModel):
    name: str
    state = Field(default=Category.PENDING)
