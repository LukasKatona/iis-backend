from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, List, Optional
from sqlmodel import Session, create_engine, select
from sqlalchemy import and_

from auth import get_current_active_user
from entities.User import User
from entities.NewCategoryRequest import NewCategoryRequest, NewCategoryRequestUpdate
from enums.CategoryRequestState import CategoryRequestState
from constants.databaseURL import DATABASE_URL

router = APIRouter()
db = create_engine(DATABASE_URL)

from fastapi import Query

@router.get("/category-requests", response_model=List[NewCategoryRequest], tags=["Category Requests"])
def get_category_requests(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    user_id: Optional[int] = Query(None), status: Optional[CategoryRequestState] = Query(None)) -> List[NewCategoryRequest]:
    
    with Session(db) as session:
        query = select(NewCategoryRequest)
        
        filters = []
        if user_id is not None:
            filters.append(NewCategoryRequest.createdById == user_id)
        if status is not None:
            filters.append(NewCategoryRequest.state == status)
        
        if filters:
            query = query.where(and_(*filters))
        
        category_requests = session.exec(query).all()
        return category_requests


@router.post("/category-requests", response_model=NewCategoryRequest, tags=["Category Requests"])
def create_category_request(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    new_request: NewCategoryRequest) -> NewCategoryRequest:
    with Session(db) as session:
        if isinstance(new_request.state, str):
            new_request.state = CategoryRequestState.strToEnum(new_request.state)     
        session.add(new_request)
        session.commit()
        session.refresh(new_request)
        return new_request

@router.patch("/category-requests/{category_id}", tags=["Category Requests"])
def update_category_request(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    category_id: int, new_category_request_update: NewCategoryRequestUpdate) -> NewCategoryRequest:
    
    if (not current_active_user.isAdmin) and (not current_active_user.isModerator):
        raise HTTPException(status_code=403, detail="You do not have permission to update category requests")
    
    with Session(db) as session:
        category_request = session.get(NewCategoryRequest, category_id)
        if isinstance(new_category_request_update.state, str):
            category_request.state = CategoryRequestState.strToEnum(new_category_request_update.state)
        else:
            category_request.state = new_category_request_update.state
        session.commit() 
        session.refresh(category_request)
        return category_request
    
@router.delete("/category-requests/{category_id}", response_model=NewCategoryRequest, tags=["Category Requests"])
def delete_category_request(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    category_id: int) -> bool:

    if (not current_active_user.isAdmin) and (not current_active_user.isModerator):
        raise HTTPException(status_code=403, detail="You do not have permission to delete category requests")

    with Session(db) as session:
        try:
            category_request = session.get(NewCategoryRequest, category_id)
            session.delete(category_request)
            session.commit()
            return True
        except:
            session.rollback()
            raise HTTPException(status_code=400, detail="Category request not found")
        
            
    
 