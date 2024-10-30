from fastapi import APIRouter, HTTPException
from typing import List, Optional
from sqlmodel import Session, create_engine, select
import datetime

from enums.OrderStatus import OrderStatus
from entities.Order import Order
from constants.databaseURL import DATABASE_URL

router = APIRouter()
db = create_engine(DATABASE_URL)

@router.get("/orders", response_model=List[Order])
def get_orders(user_id: Optional[int] = None, status: Optional[OrderStatus] = None) -> List[Order]:
    with Session(db) as session:
        query = select(Order)
        
        if user_id is not None:
            query = query.where(Order.userId == user_id)
        if status is not None:
            query = query.where(Order.status == status)
        
        return session.exec(query).all()

@router.post("/orders", response_model=Order)
def create_order(user_id: int, total_price: float):
    if total_price < 0:
        raise HTTPException(status_code=400, detail="Total price must be non-negative.")
    
    with Session(db) as session:
        new_order = Order(
            userId=user_id,
            totalPrice=total_price,
            createdAt=datetime.now()
        )
        
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        return new_order

@router.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: int, new_status: OrderStatus):
    with Session(db) as session:
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        
        order.status = new_status
        if new_status == OrderStatus.ACCEPTED:
            order.acceptedAt = datetime.now()
        
        session.commit()
        session.refresh(order)
        return order
