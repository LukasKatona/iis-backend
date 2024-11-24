from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, create_engine, select, and_
from datetime import datetime

from auth import get_current_active_user
from entities.Review import Review
from entities.User import User
from entities.Product import Product
from entities.Order import Order
from constants.databaseURL import DATABASE_URL

router = APIRouter()
db = create_engine(DATABASE_URL)

formatted_date = datetime.timestamp(datetime.now())

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
    
@router.post("/reviews", response_model=Review, tags=["Reviews"])
def create_review_for_product(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    new_review: Review) -> Review:
    if new_review.userId != current_active_user.id:
        raise HTTPException(status_code=403, detail="You can only review products as yourself.")
    if new_review.rating < 0 or new_review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
    
    with Session(db) as session:
        your_order = session.exec(select(Order).where(Order.id == new_review.orderId)).one()
        if not your_order:
            raise HTTPException(status_code=404, detail="Order not found.")
        if your_order.userId != current_active_user.id:
            raise HTTPException(status_code=403, detail="You can only review your own orders.")
        
        new_review.createdAt = formatted_date
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        return new_review
    
@router.patch("/reviews/{review_id}", response_model=Review, tags=["Reviews"])
def create_review_for_product(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    review_update: Review) -> Review:
    if review_update.userId != current_active_user.id:
        raise HTTPException(status_code=403, detail="You can only review products as yourself.")
    if review_update.rating < 0 or review_update.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
    
    with Session(db) as session:
        review = session.exec(select(Review).where(Review.id == review_update.id)).one()

        for key, value in review_update.model_dump().items():
            if value is not None:
                setattr(review, key, value)
        session.add(review)
        session.commit()
        session.refresh(review)
        return review

@router.delete("/reviews/{review_id}", response_model=Review, tags=["Reviews"])
def delete_review(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    review_id: int) -> bool:
    with Session(db) as session:
        try:        
            review = session.exec(select(Review).where(Review.id == review_id)).one()
            
            if not review:
                raise HTTPException(status_code=404, detail="Review not found.")
            
            if review.userId != current_active_user.id:
                raise HTTPException(status_code=403, detail="You can only delete your own reviews.")
            
            session.delete(review)
            session.commit()
            return True
        except:
            session.rollback()
            raise HTTPException(status_code=400, detail="Review not found")
        
