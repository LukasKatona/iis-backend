from fastapi import APIRouter, HTTPException
from typing import List, Optional
from sqlmodel import Session, create_engine, select

from entities.NewCategoryRequest import NewCategoryRequest
from enums.CategoryRequestState import CategoryRequestState
from constants.databaseURL import DATABASE_URL

router = APIRouter()
db = create_engine(DATABASE_URL)

from fastapi import Query

@router.get("/category-requests", response_model=List[NewCategoryRequest], tags=["Category Requests"])
def get_category_requests(user_id: Optional[int] = Query(None), status: Optional[CategoryRequestState] = Query(None)) -> List[NewCategoryRequest]:
    with Session(db) as session:
        query = select(NewCategoryRequest)
        
        if user_id is not None:
            query = query.where(NewCategoryRequest.createdById == user_id)
        
        if status is not None:
            query = query.where(NewCategoryRequest.state == status)
        
        category_requests = session.exec(query).all()
        return category_requests


@router.post("/category-request", response_model=NewCategoryRequest, tags=["Category Requests"])
def create_category_request(newCategoryName: str, createdById: int, parentCategoryId: Optional[int] = None, state: CategoryRequestState = CategoryRequestState.PENDING ) -> NewCategoryRequest:
    with Session(db) as session:        
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
    
@router.delete("/category-request/{category_id}", response_model=NewCategoryRequest, tags=["Category Requests"])
def delete_category_request(category_id: int) -> NewCategoryRequest:
    with Session(db) as session:
        category_request = session.get(NewCategoryRequest, category_id)
        session.delete(category_request)
        session.commit()
        return category_request
 