from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, create_engine, select, and_
import datetime

from entities.Review import Review
from constants.databaseURL import DATABASE_URL

router = APIRouter()
db = create_engine(DATABASE_URL)

@router.get("/reviews")
def get_reviews(
    userIdFilter: Optional[int] = Query(None),
    productIdFilter: Optional[int] = Query(None)
) -> List[Review]:
    with Session(db) as session:
        query = select(Review).where(Review.deletedAt.is_(None))

        filters = []
        if userIdFilter:
            filters.append(Review.userId == userIdFilter)
        if productIdFilter:
            filters.append(Review.productId == productIdFilter)
        if filters:
            query = query.where(and_(*filters))
        
        return session.exec(query).all()

@router.get("/reviews/{review_id}")
def get_review_by_id(review_id: int) -> Review:
    with Session(db) as session:
        review = session.exec(select(Review).where(Review.id == review_id, Review.deletedAt.is_(None))).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found or deleted.")
        return review

@router.post("/reviews")
def create_review(userId: int, productId: int, rating: int, review: Optional[str] = None) -> Review:
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    with Session(db) as session:
        new_review = Review(
            userId=userId,
            productId=productId,
            rating=rating,
            review=review,
            createdAt=datetime.now())
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        return new_review

@router.patch("/reviews/{review_id}")
def update_review(review_id: int, rating: Optional[int] = None, review: Optional[str] = None) -> Review:
    with Session(db) as session:
        existing_review = session.get(Review, review_id)
        if not existing_review or existing_review.deletedAt is not None:
            raise HTTPException(status_code=404, detail="Review not found or deleted.")

        if rating is not None:
            if rating < 1 or rating > 5:
                raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
            existing_review.rating = rating
        if review is not None:
            existing_review.review = review
        existing_review.updatedAt = datetime.now()

        session.commit()
        session.refresh(existing_review)
        return existing_review

@router.delete("/reviews/{review_id}")
def delete_review(review_id: int) -> Review:
    with Session(db) as session:
        existing_review = session.get(Review, review_id)
        if not existing_review or existing_review.deletedAt is not None:
            raise HTTPException(status_code=404, detail="Review not found or already deleted.")
        
        existing_review.deletedAt = datetime.now()
        session.commit()
        session.refresh(existing_review)
        return existing_review
