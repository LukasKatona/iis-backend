from fastapi import APIRouter, HTTPException
from sqlmodel import Session, create_engine, select


from entities.ProductCategory import ProductCategory
from entities.NewCategoryRequest import NewCategoryRequest
from enums.CategoryRequestState import Category

from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/product-categories")
def get_product_categories() -> list[ProductCategory]:
    with Session(db) as session:
        categories = session.exec(select(ProductCategory)).all()
        return categories

@router.post("/category-request", response_model=NewCategoryRequest)
def create_category_request(new_request: NewCategoryRequest) -> NewCategoryRequest:
    with Session(db) as session:
        existing_category = session.exec(select(NewCategoryRequest).where(NewCategoryRequest.name == new_request.name)).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this name already exists.")
        
        session.add(new_request)
        session.commit()
        session.refresh(new_request)
        return new_request

@router.patch("/category-request/{category_id}/status", response_model=NewCategoryRequest)
def update_category_request_status(category_id: int, new_state: Category) -> NewCategoryRequest:
    with Session(db) as session:
        category_request = session.get(NewCategoryRequest, category_id)
        if not category_request:
            raise HTTPException(status_code=404, detail="Category request not found.")
        
        category_request.state = new_state
        session.commit()
        session.refresh(category_request)
        return category_request