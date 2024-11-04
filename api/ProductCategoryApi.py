# library imports
from fastapi import APIRouter
from sqlmodel import Session, create_engine, select

# local imports
from entities.ProductCategory import ProductCategory, ProductCategoryUpdate
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/product-categories", tags=["Product Categories"])
def get_product_categories() -> list[ProductCategory]:
    with Session(db) as session:
        return session.exec(select(ProductCategory)).all()
    
@router.post("/product-categories", tags=["Product Categories"])
def create_product_category(category: ProductCategory) -> ProductCategory:
    with Session(db) as session:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    
@router.patch("/product-categories/{category_id}", tags=["Product Categories"])
def update_product_category(
    category_id: int,
    category_update: ProductCategoryUpdate
) -> ProductCategory:
    with Session(db) as session:
        category = session.exec(select(ProductCategory).where(ProductCategory.id == category_id)).one()
        for key, value in category_update.model_dump().items():
            if value is not None:
                setattr(category, key, value)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    
@router.delete("/product-categories/{category_id}", tags=["Product Categories"])
def delete_product_category(
    category_id: int,
) -> bool:
    with Session(db) as session:
        try:
            category = session.exec(select(ProductCategory).where(ProductCategory.id == category_id)).one()
            delete_child_categories(category, session)
            session.delete(category)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False
        
    
def delete_child_categories(category: ProductCategory, session: Session):
    for child in category.childCategories:
        delete_child_categories(child, session)
        session.delete(child)
