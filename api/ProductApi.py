# library imports
from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import and_
from sqlmodel import Session, create_engine, select
from enums.Unit import Unit

# local imports
from entities.ProductCategory import ProductCategory
from entities.Product import Product, ProductUpdate
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/products", tags=["Products"])
def get_products(
    nameFilter: Optional[str] = Query(None),
    categoryIdFilter: Optional[int] = Query(None),
    farmerIdFilter: Optional[int] = Query(None),
    sortField: Optional[str] = Query(None),
    sortDirection: Optional[str] = Query(None)
) -> list[Product]:
    with Session(db) as session:
        query = select(Product)

        # apply filters
        if nameFilter or categoryIdFilter or farmerIdFilter:
            filters = []
            if nameFilter:
                filters.append(Product.name == nameFilter)
            if categoryIdFilter:
                category = session.exec(select(ProductCategory).where(ProductCategory.id == categoryIdFilter)).first()
                filters.append(Product.categoryId.in_(get_subcategory_ids(category)))
            if farmerIdFilter:
                filters.append(Product.farmerId == farmerIdFilter)
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
    
@router.post("/products", tags=["Products"])
def create_product(product: Product) -> Product:
    with Session(db) as session:
        if isinstance(product.unit, str):
            product.unit = Unit.strToEnum(product.unit)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    
@router.patch("/products/{product_id}", tags=["Products"])
def update_product(
    product_id: int,
    product_update: ProductUpdate
) -> Product:
    with Session(db) as session:
        product = session.exec(select(Product).where(Product.id == product_id)).one()
        for key, value in product_update.model_dump().items():
            if value is not None:
                setattr(product, key, value)
        if isinstance(product.unit, str):
            product.unit = Unit.strToEnum(product.unit)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    
@router.delete("/products/{product_id}", tags=["Products"])
def delete_product(
    product_id: int,
) -> bool:
    with Session(db) as session:
        try:
            product = session.exec(select(Product).where(Product.id == product_id)).one()
            session.delete(product)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False