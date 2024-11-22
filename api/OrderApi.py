from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated, List, Optional
from sqlalchemy import and_
from sqlmodel import Session, create_engine, select
from datetime import datetime

from enums.OrderStatus import OrderStatus
from entities.Order import Order, OrderUpdate
from entities.Farmer import Farmer
from entities.OrderProductRelation import OrderProductRelation, OrderProductRelationUpdate
from entities.Product import Product, ProductWithQuantity
from auth import get_current_active_user
from entities.User import User
from entities.Review import Review
from constants.databaseURL import DATABASE_URL

router = APIRouter()
db = create_engine(DATABASE_URL)

formatted_date = datetime.timestamp(datetime.now())

def generate_order_number() -> str:
    return f"ORD-{int(datetime.now().timestamp())}"

@router.get("/orders", response_model=List[Order], tags=['Orders'])
def get_orders(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    user_id: Optional[int] = None, farmer_id: Optional[int] = None, status: Optional[OrderStatus] = None, exclude_status: Optional[OrderStatus] = None) -> List[Order]:
    
    with Session(db) as session:
        query = select(Order)
        filters = []
        
        if user_id:
            filters.append(Order.userId == user_id)
        if farmer_id:
            filters.append(Order.farmerId == farmer_id)
        if status:
            filters.append(Order.status == status)
        if exclude_status: 
            filters.append(Order.status != exclude_status)
            
        if filters:
            query = query.where(*filters)
        
        return session.exec(query).all()


@router.patch("/orders/{order_id}/status", tags=['Orders'])
def update_order_status(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    order_id: int, new_status_update: OrderUpdate) -> Order:
    with Session(db) as session:
        order = session.get(Order, order_id)
       
        if isinstance(new_status_update.status, str):
            new_status_update = OrderStatus.strToEnum(new_status_update.status)

        order.status = new_status_update.status
        order.updatedAt = formatted_date
        
        if new_status_update.status == OrderStatus.SUPPLIED:
            order.suppliedAt = formatted_date
          
        session.commit()
        session.refresh(order)

        return order


@router.post("/orders/add-product", response_model=Order, tags=['Orders'])
def add_product_to_order(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int, product_id: int, quantity: int):
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
def update_product_in_order(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    order_id: int, product_update: OrderProductRelationUpdate):
    with Session(db) as session:
        order = session.get(Order, order_id)
        product = session.get(Product, product_update.productId)
        
        relation = session.exec(
            select(OrderProductRelation)
            .where(OrderProductRelation.orderId == order_id, OrderProductRelation.productId == product_update.productId)
        ).first()

        if product.stock < product_update.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        current_quantity = relation.quantity
        relation.quantity = product_update.quantity	
        product.stock = product.stock - (product_update.quantity - current_quantity)

        if product_update.quantity == 0:
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

@router.delete("/orders/{order_id}", tags=['Orders'])
def delete_order(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    order_id: int) -> bool:
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
            raise HTTPException(status_code=400, detail="Order not found")

@router.delete("/orders/{order_id}/product/{product_id}", response_model=Order, tags=['Orders'])
def delete_product_from_order(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    order_id: int, product_id: int):
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
    
@router.get("/orders/{order_id}/products", response_model=List[ProductWithQuantity], tags=["Orders"])
def get_products_of_order(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    order_id: int):
    with Session(db) as session:
        relations = session.exec(
            select(OrderProductRelation).where(OrderProductRelation.orderId == order_id)
        ).all()
        
        product_ids = [relation.productId for relation in relations]
        products = session.exec(
            select(Product).where(Product.id.in_(product_ids))
        ).all()
        
        products_with_quantity = []
        
        for relation in relations:
            product = next((p for p in products if p.id == relation.productId), None)
            if product:
                product_review = session.exec(
                    select(Review).where(and_(Review.productId == product.id, Review.orderId == order_id, Review.userId == current_active_user.id))
                ).first()
                products_with_quantity.append(ProductWithQuantity(product=product, quantity=relation.quantity, review=product_review))
        return products_with_quantity

@router.get("/orders/number-of-products", response_model=int, tags=["Orders"])
def get_number_of_products_in_my_order(
    current_active_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(db) as session:
        my_orders = session.exec(
            select(Order).where(Order.userId == current_active_user.id, Order.status == OrderStatus.IN_CART)
        ).all()

        if not my_orders:
            return 0

        sum = 0
        for order in my_orders:
            relations = session.exec(
                select(OrderProductRelation).where(OrderProductRelation.orderId == order.id)
            ).all()
            sum += len(relations)

        return sum