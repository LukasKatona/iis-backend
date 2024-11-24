# library imports
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, asc, desc
from sqlmodel import Session, create_engine, select


# local imports
from entities.Farmer import Farmer
from entities.ProductCategory import ProductCategory
from entities.Product import Product, ProductUpdate, ProductWithRating
from constants.databaseURL import DATABASE_URL
from auth import get_current_active_user
from entities.User import User
from entities.Review import Review
from enums.Unit import Unit

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/products", tags=["Products"])
def get_products(
    nameFilter: Optional[str] = Query(None),
    categoryIdFilter: Optional[int] = Query(None),
    farmerIdFilter: Optional[int] = Query(None),
    sortField: Optional[str] = Query(None),
    sortDirection: Optional[str] = Query(None)
) -> list[ProductWithRating]:
    with Session(db) as session:
        query = select(Product)

        # apply filters
        if nameFilter or categoryIdFilter or farmerIdFilter:
            filters = []
            if nameFilter:
                filters.append(Product.name == nameFilter)
            if categoryIdFilter:
                category = session.exec(select(ProductCategory).where(ProductCategory.id == categoryIdFilter)).one()
                filters.append(Product.categoryId.in_(get_subcategory_ids(category)))
            if farmerIdFilter:
                filters.append(Product.farmerId == farmerIdFilter)
            query = query.where(and_(*filters))
        
        if sortField and sortField != "rating":
            column = getattr(Product, sortField, None) 
            if column:
                if sortDirection == "asc":
                    query = query.order_by(asc(column))
                else:
                    query = query.order_by(desc(column))

        # get products with rating
        products_with_rating = []  
        products = session.exec(query).all()
        for product in products:
            product_reviews = session.exec(select(Review).where(Review.productId == product.id)).all()
            if len(product_reviews) > 0:
                rating = sum([review.rating for review in product_reviews]) / len(product_reviews)
            else:
                rating = 0
            products_with_rating.append(ProductWithRating(**product.model_dump(), rating=rating))

        if sortField == "rating":
            if sortDirection == "asc":
                products_with_rating.sort(key=lambda x: x.rating, reverse=False)
            else:
                products_with_rating.sort(key=lambda x: x.rating, reverse=True)
        
        return products_with_rating
    
@router.get("/products/most-popular", tags=["Products"])
def get_products() -> list[ProductWithRating]:
    with Session(db) as session:
        query = select(Product)

        # get products with rating
        products_with_rating = []  
        products = session.exec(query).all()
        for product in products:
            product_reviews = session.exec(select(Review).where(Review.productId == product.id)).all()
            if len(product_reviews) > 0:
                rating = sum([review.rating for review in product_reviews]) / len(product_reviews)
            else:
                rating = 0
            products_with_rating.append(ProductWithRating(**product.model_dump(), rating=rating))

        products_with_rating.sort(key=lambda x: x.rating, reverse=True)
        products_with_rating = [product for product in products_with_rating if product.rating > 0]
        
        return products_with_rating[:5]

def get_subcategory_ids(category: ProductCategory) -> list[int]:
    subcategory_ids = [category.id]

    for subcategory in category.childCategories:
        subcategory_ids.extend(get_subcategory_ids(subcategory))
    
    return subcategory_ids
  
@router.get("/products/{product_id}", tags=["Products"])
def get_product_by_id(product_id: int) -> Product:
    with Session(db) as session:
        return session.exec(select(Product).where(Product.id == product_id)).one()
    
@router.post("/products", tags=["Products"])
def create_product(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    product: Product) -> Product:
    if (not current_active_user.isFarmer):
        raise HTTPException(status_code=403, detail="You do not have permission to create a product.")
    
    if product.categoryAtributes == '':
        product.categoryAtributes = None

    with Session(db) as session:
        if isinstance(product.unit, str):
            product.unit = Unit.strToEnum(product.unit)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    
@router.patch("/products/{product_id}", tags=["Products"])
def update_product(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    product_id: int,
    product_update: ProductUpdate
) -> Product:
    if (not current_active_user.isFarmer):
        raise HTTPException(status_code=403, detail="You do not have permission to update a product.")

    with Session(db) as session:
        product = session.exec(select(Product).where(Product.id == product_id)).one()

        if (product.farmerId != current_active_user.farmerId):
            raise HTTPException(status_code=403, detail="You do not have permission to update this product.")

        for key, value in product_update.model_dump().items():
            if value is not None:
                setattr(product, key, value)
        if isinstance(product.unit, str):
            product.unit = Unit.strToEnum(product.unit)
        if product.categoryAtributes == '':
            product.categoryAtributes = None
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    
@router.delete("/products/{product_id}", tags=["Products"])
def delete_product(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    product_id: int,
) -> bool:
    if (not current_active_user.isFarmer):
        raise HTTPException(status_code=403, detail="You do not have permission to delete a product.")
    
    with Session(db) as session:
        try:
            product = session.exec(select(Product).where(Product.id == product_id)).one()

            if (product.farmerId != current_active_user.farmerId):
                raise HTTPException(status_code=403, detail="You do not have permission to delete this product.")
            
            session.delete(product)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail="Product not found")
