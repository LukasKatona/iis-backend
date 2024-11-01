from fastapi import APIRouter, HTTPException
from typing import List, Optional
from sqlmodel import Session, create_engine, select

from entities.NewCategoryRequest import NewCategoryRequest
from enums.CategoryRequestState import CategoryRequestState
from constants.databaseURL import DATABASE_URL

router = APIRouter()
db = create_engine(DATABASE_URL)

@router.get("/category-requests", response_model=List[NewCategoryRequest], tags=["Category Requests"])
def get_category_requests() -> List[NewCategoryRequest]:
    with Session(db) as session:
        category_requests = session.exec(select(NewCategoryRequest)).all()
        return category_requests

@router.post("/category-request", response_model=NewCategoryRequest, tags=["Category Requests"])
def create_category_request(newCategoryName: str, createdById: int, parentCategoryId: Optional[int] = None, state: CategoryRequestState = CategoryRequestState.PENDING ) -> NewCategoryRequest:
    with Session(db) as session:
        # existing_request = session.exec(
        #     select(NewCategoryRequest).where(NewCategoryRequest.newCategoryName == newCategoryName)
        # ).first()
        
        # if existing_request:
        #     raise HTTPException(status_code=400, detail="Category request with this name already exists.")
        
        new_request = NewCategoryRequest(
            newCategoryName=newCategoryName,
            parentCategoryId=parentCategoryId,
            createdById=createdById,
            state=state
        )
        
        session.add(new_request)
        session.commit()
        session.refresh(new_request)
        return new_request

@router.patch("/category-request/{category_id}/status", response_model=NewCategoryRequest, tags=["Category Requests"])
def update_category_request_status(category_id: int, new_state: CategoryRequestState) -> NewCategoryRequest:
    with Session(db) as session:
        category_request = session.get(NewCategoryRequest, category_id)
        category_request.state = new_state
        session.commit()
        session.refresh(category_request)
        return category_request
