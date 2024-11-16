from fastapi import APIRouter, HTTPException, Response
from typing import List, Optional
from sqlmodel import Session, create_engine, select
from datetime import datetime
from constants.databaseURL import DATABASE_URL

from enums.OrderStatus import OrderStatus
from entities.Order import Order, OrderUpdate
from entities.Farmer import Farmer
from entities.OrderProductRelation import OrderProductRelation
from entities.Product import Product

router = APIRouter()
db = create_engine(DATABASE_URL)

formatted_date = datetime.timestamp(datetime.now())

def generate_order_number() -> str:
    return f"ORD-{int(datetime.now().timestamp())}"

@router.get("/orders", response_model=List[Order], tags=['Orders'])
def get_orders(user_id: Optional[int] = None, farmer_id: Optional[int] = None, status: Optional[OrderStatus] = None) -> List[Order]:
    with Session(db) as session:
        query = select(Order)
        filters = []
        
        if user_id:
            filters.append(Order.userId == user_id)
        if farmer_id:
            filters.append(Order.farmerId == farmer_id)
        if status:
            filters.append(Order.status == status)
            
        if filters:
            query = query.where(*filters)
        
        return session.exec(query).all()


@router.patch("/orders/{order_id}/status", tags=['Orders'])
def update_order_status(order_id: int, new_status_update: OrderUpdate) -> Order:
    with Session(db) as session:
        order = session.get(Order, order_id)
       
        if isinstance(new_status_update.status, str):
            new_status_update = OrderStatus.strToEnum(new_status_update.status)


        order.status = new_status_update.status
        
        if new_status_update.status == OrderStatus.ACCEPTED:
            order.suppliedAt = formatted_date
            
        session.commit()
        session.refresh(order)

        return order


@router.post("/orders/add-product", response_model=Order, tags=['Orders'])
def add_product_to_order(user_id: int, product_id: int, quantity: int):
    
    with Session(db) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")
        
        existing_order = session.exec(
            select(Order).where(
                Order.userId == user_id, 
                Order.farmerId == product.farmerId,
                Order.status == OrderStatus.IN_CART
            )
        ).first()
        
        if not existing_order or existing_order.status != OrderStatus.IN_CART:
            existing_order = Order(
                orderNumber=generate_order_number(),
                userId=user_id,
                farmerId=product.farmerId,
                status=OrderStatus.IN_CART,
                createdAt=formatted_date
            )
            session.add(existing_order)
            session.commit()
            session.refresh(existing_order)
        

        relation = session.exec(
            select(OrderProductRelation)
            .where(OrderProductRelation.orderId == existing_order.id, OrderProductRelation.productId == product_id)
        ).first()
        
        if relation:
            relation.quantity += quantity
        else:
            relation = OrderProductRelation(orderId=existing_order.id, productId=product.id, quantity=quantity)
            session.add(relation)
        
        product.stock -= quantity
        session.add(product)
        session.commit()
        session.refresh(existing_order)
        
        return existing_order

@router.patch("/orders/{order_id}/edit-product", response_model=Order, tags=['Orders'])
def update_product_in_order(order_id: int, product_id: int, quantity: int):
    with Session(db) as session:
        order = session.get(Order, order_id)
        product = session.get(Product, product_id)
        
        relation = session.exec(
            select(OrderProductRelation)
            .where(OrderProductRelation.orderId == order_id, OrderProductRelation.productId == product_id)
        ).first()

        if product.stock < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        current_quantity = relation.quantity
        relation.quantity = quantity
        product.stock = product.stock - (quantity - current_quantity)

        if quantity == 0:
            session.delete(relation)
            session.commit()

            remaining_products = session.exec(
                select(OrderProductRelation).where(OrderProductRelation.orderId == order_id)
            ).all()
            
            if not remaining_products:
                session.delete(order)
                session.commit()
                return Response(status_code=204, content="Order deleted, because last product was removed.")
                

        session.commit()
        if order in session:
            session.refresh(order)
        
        return order

@router.delete("/orders/{order_id}", response_model=Order, tags=['Orders'])
def delete_order(order_id: int) -> bool:
    with Session(db) as session:
        try:
            order = session.get(Order, order_id)
      
            if order.status != OrderStatus.IN_CART:
                raise HTTPException(status_code=403, detail="Only 'IN_CART' can be deleted.")
            
            order_products = session.exec(
                select(OrderProductRelation).where(OrderProductRelation.orderId == order_id)
            ).all()
            
            for relation in order_products:
                product = session.get(Product, relation.productId)
                if product:
                    product.stock += relation.quantity
                    session.add(product)
                session.delete(relation)
            session.delete(order)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False

@router.delete("/orders/{order_id}/product/{product_id}", response_model=Order, tags=['Orders'])
def delete_product_from_order(order_id: int, product_id: int):
    with Session(db) as session:
        order = session.get(Order, order_id)
       
        if order.status != OrderStatus.IN_CART:
            raise HTTPException(status_code=400, detail="only 'IN_CART'.")

        relation = session.exec(
            select(OrderProductRelation)
            .where(OrderProductRelation.orderId == order_id, OrderProductRelation.productId == product_id)
        ).first()
        
        product = session.get(Product, product_id)
        if product:
            product.stock += relation.quantity
        
        session.add(product)
        session.delete(relation)
        session.commit()
        
        remaining_products = session.exec(
            select(OrderProductRelation).where(OrderProductRelation.orderId == order_id)
        ).all()
        
        if not remaining_products:
            session.delete(order)
            return Response(status_code=204, content="Order deleted, because last product was removed.")
        
        session.commit()
        session.refresh(order)
        
        return order
    
@router.get("/orders/{order_id}/products", response_model=List[Product], tags=["Orders"])
def get_products_of_order(order_id: int):
    with Session(db) as session:
        relations = session.exec(
            select(OrderProductRelation).where(OrderProductRelation.orderId == order_id)
        ).all()
        
        product_ids = [relation.productId for relation in relations]
        products = session.exec(
            select(Product).where(Product.id.in_(product_ids))
        ).all()
        
        for relation in relations:
            product = next((p for p in products if p.id == relation.productId), None)
            if product:
                product.stock = relation.quantity
        return products
