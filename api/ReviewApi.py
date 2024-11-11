from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, create_engine, select, and_
from datetime import datetime

from entities.Review import Review
from entities.User import User
from entities.Product import Product
from entities.Order import Order
from constants.databaseURL import DATABASE_URL

router = APIRouter()
db = create_engine(DATABASE_URL)

formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M")

@router.get("/reviews", response_model=List[Review], tags=["Reviews"])
def get_reviews(userIdFilter: Optional[int] = Query(None), productIdFilter: Optional[int] = Query(None), orderIdFilter: Optional[int] = Query(None)) -> List[Review]:
    with Session(db) as session:
        query = select(Review)
        filters = []

        if userIdFilter:
            filters.append(Review.userId == userIdFilter)
        if productIdFilter:
            filters.append(Review.productId == productIdFilter)
        if orderIdFilter:
            filters.append(Review.orderId == orderIdFilter)

        if filters:
            query = query.where(and_(*filters))
        
        return session.exec(query).all()

@router.post("/reviews/order/{order_id}", response_model=Review, tags=["Reviews"])
def create_review_for_order(userId: int, orderId: int, rating: int, review: Optional[str] = None) -> Review:
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    with Session(db) as session:
        new_review = Review(
            userId=userId,
            orderId=orderId,
            rating=rating,
            review=review,
            createdAt=formatted_date
        )
        
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        return new_review
    
@router.post("/reviews/product/{product_id}", response_model=Review, tags=["Reviews"])
def create_review_for_product(userId: int, orderId: int, productId: int, rating: int, review: Optional[str] = None) -> Review:
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
    
    with Session(db) as session:
        new_review = Review(
            userId=userId,
            orderId=orderId,
            productId=productId,
            rating=rating,
            review=review,
            createdAt=formatted_date
        )
        
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        return new_review

@router.delete("/reviews/{review_id}", response_model=Review, tags=["Reviews"])
def delete_review(review_id: int, product_id: Optional[int] = None, order_id: Optional[int] = None) -> bool:
    with Session(db) as session:
        try:        
            review = session.exec(select(Review).where(Review.id == review_id)).one()
            
            if not review:
                raise HTTPException(status_code=404, detail="Review not found.")
            
            session.delete(review)
            session.commit()
            return True
        except:
            session.rollback()
            return False
        
