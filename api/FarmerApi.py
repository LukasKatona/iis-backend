# library imports
from typing import Annotated, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, or_
from sqlmodel import Session, create_engine, select

# local imports
from auth import get_current_active_user
from entities.User import User
from entities.Farmer import Farmer, FarmerUpdate
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/farmers", tags=["Farmers"])
def get_farmers(
    nameFilter: Optional[str] = Query(None),
    sortField: Optional[str] = Query(None),
    sortDirection: Optional[str] = Query(None)
) -> list[Farmer]:
    with Session(db) as session:
        query = select(Farmer)

        # apply filters
        if nameFilter:
            query = query.where(Farmer.farmName == nameFilter)
        
        # apply sorting
        if sortField and sortDirection:
            if sortDirection == "asc":
                query = query.order_by(sortField)
            else:
                query = query.order_by(sortField.desc())
            
        return session.exec(query).all()

@router.get("/farmers/{farmer_id}", tags=["Farmers"])
def get_farmer_by_id(farmer_id: int) -> Farmer:
    with Session(db) as session:
        return session.exec(select(Farmer).where(Farmer.id == farmer_id)).one()
    
@router.get("/farmers/{user_id}/by-user-id", tags=["Farmers"])
def get_farmer_by_user_id(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int) -> Union[Farmer, None]:

    if current_active_user.id != user_id and not current_active_user.isAdmin:
        raise HTTPException(status_code=403, detail="You can only view your own farmer profile")

    with Session(db) as session:
        return session.exec(select(Farmer).where(Farmer.userId == user_id)).first()
    
@router.post("/farmers", tags=["Farmers"])
def create_farmer(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    farmer: Farmer) -> Farmer:

    if current_active_user.id != farmer.userId and not current_active_user.isAdmin:
        raise HTTPException(status_code=403, detail="You can only create a farmer profile for yourself")

    if not farmer.userId:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    with Session(db) as session:            
        session.add(farmer)
        session.commit()
        session.refresh(farmer)
        return farmer

@router.patch("/farmers/{farmer_id}", tags=["Farmers"])
def update_farmer(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    farmer_id: int, farmer_update: FarmerUpdate) -> Farmer:
    with Session(db) as session:
        farmer = session.exec(select(Farmer).where(Farmer.id == farmer_id)).one()

        if current_active_user.id != farmer.userId and not current_active_user.isAdmin:
            raise HTTPException(status_code=403, detail="You can only update your own farmer profile")
        
        for key, value in farmer_update.model_dump().items():
            if value is not None:
                setattr(farmer, key, value)
        
        session.commit()
        session.refresh(farmer)
        return farmer

@router.delete("/farmers/{farmer_id}", tags=["Farmers"])
def delete_farmer(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    farmer_id: int) -> bool:

    if not current_active_user.isAdmin:
        raise HTTPException(status_code=403, detail="You do not have permission to delete farmer profiles")

    with Session(db) as session:
        try:
            farmer = session.exec(select(Farmer).where(Farmer.id == farmer_id)).one()
            session.delete(farmer)
            session.commit()
            return True
        except:
            session.rollback()
            return False