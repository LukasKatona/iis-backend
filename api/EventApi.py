# library imports
import time
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_
from sqlmodel import Session, create_engine, select

# local imports
from auth import get_current_active_user
from entities.Farmer import Farmer
from entities.User import User
from entities.Event import Event, EventUpdate
from entities.UserEventRelation import UserEventRelation
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/events", tags=["Events"])
def get_events(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    nameFilter: Optional[str] = Query(None),
    createdByIdFilter: Optional[int] = Query(None),
    sortField: Optional[str] = Query(None),
    sortDirection: Optional[str] = Query(None)
) -> list[Event]:
    with Session(db) as session:
        query = select(Event)

        # apply filters
        if nameFilter or createdByIdFilter:
            filters = []
            if nameFilter:
                filters.append(Event.name == nameFilter)
            if createdByIdFilter:
                filters.append(Event.createdById == createdByIdFilter)
            query = query.where(and_(*filters))
        
        # apply sorting
        if sortField and sortDirection:
            if sortDirection == "asc":
                query = query.order_by(sortField)
            else:
                query = query.order_by(sortField.desc())
            
        return session.exec(query).all()
    
@router.get("/events/{user_id}", tags=["Events"])
def get_events_by_user(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int) -> list[Event]:
    with Session(db) as session:
        query = select(Event).join(UserEventRelation).where(UserEventRelation.userId == user_id)
        return session.exec(query).all()
    
@router.post("/events", tags=["Events"])
def create_event(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    event: Event) -> Event:
    if not current_active_user.isFarmer:
        raise HTTPException(status_code=403, detail="You do not have permission to create an event")

    with Session(db) as session:
        event.createdAt = time.time()
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

@router.patch("/events/{event_id}", tags=["Events"])
def update_event(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    event_id: int,
    event_update: EventUpdate,
) -> Event:
    with Session(db) as session:
        event = session.exec(select(Event).where(Event.id == event_id)).one()

        if event.createdById != current_active_user.farmerId:
            raise HTTPException(status_code=403, detail="You can only update events that you created")

        for key, value in event_update.model_dump().items():
            if value is not None:
                setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    
@router.delete("/events/{event_id}", tags=["Events"])
def delete_event(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    event_id: int) -> bool:
    with Session(db) as session:
        try:
            event = session.exec(select(Event).where(Event.id == event_id)).one()

            if event.createdById != current_active_user.farmerId:
                raise HTTPException(status_code=403, detail="You can only delete events that you created")

            session.delete(event)
            session.commit()
            return True
        except:
            session.rollback()
            raise HTTPException(status_code=400, detail="Event not found")
        
@router.post("/events/{event_id}/join/{user_id}", tags=["Events"])
def join_event(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    event_id: int,
    user_id: int
) -> bool:
    if current_active_user.id != user_id:
        raise HTTPException(status_code=403, detail="You can only join events as yourself")

    with Session(db) as session:
        try:
            session.add(UserEventRelation(userId=user_id, eventId=event_id))
            session.commit()
            return True
        except:
            session.rollback()
            raise HTTPException(status_code=400, detail="Event not found")
        
@router.delete("/events/{event_id}/leave/{user_id}", tags=["Events"])
def leave_event(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    event_id: int,
    user_id: int
) -> bool:
    if current_active_user.id != user_id:
        raise HTTPException(status_code=403, detail="You can only leave events as yourself")

    with Session(db) as session:
        try:
            relation = session.exec(select(UserEventRelation).where(and_(UserEventRelation.eventId == event_id, UserEventRelation.userId == user_id))).one()
            session.delete(relation)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail="Event not found")
