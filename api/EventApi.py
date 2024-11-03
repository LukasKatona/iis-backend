# library imports
from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import and_
from sqlmodel import Session, create_engine, select

# local imports
from entities.Event import Event, EventUpdate
from entities.UserEventRelation import UserEventRelation
from constants.databaseURL import DATABASE_URL

router = APIRouter()

db = create_engine(DATABASE_URL)

@router.get("/events", tags=["Events"])
def get_events(
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
def get_events_by_user(user_id: int) -> list[Event]:
    with Session(db) as session:
        query = select(Event).join(UserEventRelation).where(UserEventRelation.userId == user_id)
        return session.exec(query).all()
    
@router.post("/events", tags=["Events"])
def create_event(event: Event) -> Event:
    with Session(db) as session:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

@router.patch("/events/{event_id}", tags=["Events"])
def update_event(
    event_id: int,
    event_update: EventUpdate,
) -> Event:
    with Session(db) as session:
        event = session.exec(select(Event).where(Event.id == event_id)).one()
        for key, value in event_update.model_dump().items():
            if value is not None:
                setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    
@router.delete("/events/{event_id}", tags=["Events"])
def delete_event(event_id: int) -> bool:
    with Session(db) as session:
        try:
            event = session.exec(select(Event).where(Event.id == event_id)).one()
            session.delete(event)
            session.commit()
            return True
        except:
            session.rollback()
            return False
