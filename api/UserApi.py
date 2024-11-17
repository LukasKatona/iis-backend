# library imports
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, or_
from sqlmodel import Session, create_engine, select

# local imports
from auth import get_current_user
from entities.User import User, UserUpdate
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/users", tags=["Users"])
def get_users(
    nameFilter: Optional[str] = Query(None),
    roleFilter: Optional[str] = Query(None),
    sortField: Optional[str] = Query(None),
    sortDirection: Optional[str] = Query(None)
) -> list[User]:
    with Session(db) as session:
        query = select(User)

        # apply filters
        if nameFilter or roleFilter:
            filters = []
            if nameFilter:
                filters.append(or_(User.name == nameFilter, User.surname == nameFilter))
            if roleFilter:
                if roleFilter == "admin":
                    filters.append(User.isAdmin == True)
                elif roleFilter == "moderator":
                    filters.append(User.isModerator == True)
                elif roleFilter == "farmer":
                    filters.append(User.isFarmer == True)
                elif roleFilter == "customer":
                    filters.append(and_(User.isAdmin == False, User.isModerator == False, User.isFarmer == False))
            query = query.where(and_(*filters))
        
        # apply sorting
        if sortField and sortDirection:
            if sortDirection == "asc":
                query = query.order_by(sortField)
            else:
                query = query.order_by(sortField.desc())
            
        return session.exec(query).all()
    
@router.get("/users/me", tags=["Users"])
def get_logged_in_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user

@router.get("/users/{user_id}", tags=["Users"])
def get_user_by_id(user_id: int) -> User:
    with Session(db) as session:
        return session.exec(select(User).where(User.id == user_id)).one()
    
@router.post("/users", tags=["Users"])
def create_user(user: User) -> User:
    with Session(db) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
@router.patch("/users/{user_id}", tags=["Users"])
def update_user(user_id: int, user_update: UserUpdate) -> User:
    with Session(db) as session:
        user = session.exec(select(User).where(User.id == user_id)).one()
        
        for key, value in user_update.model_dump().items():
            setattr(user, key, value)

        session.commit()
        session.refresh(user)
        return user
    
@router.patch("/users/{user_id}/password", tags=["Users"])
def change_user_password(
    user_id: int,
    old_password: str,
    new_password: str
) -> User:
    with Session(db) as session:
        user = session.exec(select(User).where(User.id == user_id)).one()
        if user.password != old_password:
            raise HTTPException(status_code=401, detail="Old password is incorrect.")
        user.password = new_password
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

#delete
@router.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int) -> bool:
    with Session(db) as session:
        try:
            user = session.exec(select(User).where(User.id == user_id)).one()
            if user.isAdmin:
                raise HTTPException(status_code=403, detail="Admin user cannot be deleted.")
            session.delete(user)
            session.commit()
            return True
        except:
            session.rollback()
            return False
