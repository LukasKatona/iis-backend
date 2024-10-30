# library imports
from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import and_, or_
from sqlmodel import Session, create_engine, select

# local imports
from entities.ProductCategory import ProductCategory
from entities.Product import Product
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/products", tags=["Products"])
def get_products(
    nameFilter: Optional[str] = Query(None),
    categoryIdFilter: Optional[int] = Query(None),
    sortField: Optional[str] = Query(None),
    sortDirection: Optional[str] = Query(None)
) -> list[Product]:
    with Session(db) as session:
        query = select(Product)

        # apply filters
        if nameFilter or categoryIdFilter:
            filters = []
            if nameFilter:
                filters.append(Product.name == nameFilter)
            if categoryIdFilter:
                category = session.exec(select(ProductCategory).where(ProductCategory.id == categoryIdFilter)).first()
                filters.append(Product.categoryId.in_(get_subcategory_ids(category)))
            query = query.where(and_(*filters))
        
        # apply sorting
        if sortField and sortDirection:
            if sortDirection == "asc":
                query = query.order_by(sortField)
            else:
                query = query.order_by(sortField.desc())
            
        return session.exec(query).all()

def get_subcategory_ids(category: ProductCategory) -> list[int]:
    subcategory_ids = [category.id]

    for subcategory in category.childCategories:
        subcategory_ids.extend(get_subcategory_ids(subcategory))
    
    return subcategory_ids

    
@router.get("/products/{product_id}", tags=["Products"])
def get_product_by_id(product_id: int) -> Product:
    with Session(db) as session:
        return session.exec(select(Product).where(Product.id == product_id)).first()
    