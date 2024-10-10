# library imports
from fastapi import APIRouter
from sqlmodel import Session, create_engine, select

# local imports
from entities.ProductCategory import ProductCategory
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/product-categories")
def get_product_categories() -> list[ProductCategory]:
    with Session(db) as session:
        return session.exec(select(ProductCategory)).all()

    
@router.get("/product-categories/{category_id}")
def get_product_category_by_id(category_id: int) -> ProductCategory:
    with Session(db) as session:
        return session.exec(select(ProductCategory).where(ProductCategory.id == category_id)).first()
    
@router.post("/product-categories/")
def create_product_category(product_category: ProductCategory):
    with Session(db) as session:
        session.add(product_category)
        session.commit()
        session.refresh(product_category)
        return product_category