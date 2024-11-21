# library imports
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlmodel import Session, create_engine, select

# local imports
from auth import get_current_active_user
from api.ProductApi import get_subcategory_ids
from entities.Product import Product
from entities.User import User
from entities.ProductCategory import ProductCategory, ProductCategoryUpdate
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/product-categories", tags=["Product Categories"])
def get_product_categories() -> list[ProductCategory]:
    with Session(db) as session:
        return session.exec(select(ProductCategory)).all()
    
@router.post("/product-categories", tags=["Product Categories"])
def create_product_category(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    category: ProductCategory) -> ProductCategory:
    if (not current_active_user.isAdmin) and (not current_active_user.isModerator):
        raise Exception("You do not have permission to create a product category.")

    with Session(db) as session:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    
@router.patch("/product-categories/{category_id}", tags=["Product Categories"])
def update_product_category(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    category_id: int,
    category_update: ProductCategoryUpdate
) -> ProductCategory:
    if (not current_active_user.isAdmin) and (not current_active_user.isModerator):
        raise Exception("You do not have permission to update a product category.")

    with Session(db) as session:
        category = session.exec(select(ProductCategory).where(ProductCategory.id == category_id)).one()
        
        products_in_category = session.exec(select(Product).where(Product.categoryId == category_id)).all()
        if len(products_in_category) > 0 and category.atributes != category_update.atributes:
            print(category.atributes)
            raise HTTPException(status_code=409, detail="Cannot update category attributes because there are products in this category.")

        for key, value in category_update.model_dump().items():
            if value is not None:
                setattr(category, key, value)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    
@router.delete("/product-categories/{category_id}", tags=["Product Categories"])
def delete_product_category(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    category_id: int,
) -> bool:
    if (not current_active_user.isAdmin) and (not current_active_user.isModerator):
        raise Exception("You do not have permission to delete a product category.")

    with Session(db) as session:
        try:
            category = session.exec(select(ProductCategory).where(ProductCategory.id == category_id)).one()
            
            query = select(Product)
            filters = []
            filters.append(Product.categoryId.in_(get_subcategory_ids(category)))
            query = query.where(and_(*filters))
            products = session.exec(query).all()
            if len(products) > 0:
                raise HTTPException(status_code=409, detail="Cannot delete category because there are products in this category.")
            
            delete_child_categories(category, session)
            session.delete(category)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e;
        
    
def delete_child_categories(category: ProductCategory, session: Session):
    for child in category.childCategories:
        delete_child_categories(child, session)
        session.delete(child)
