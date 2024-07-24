from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from datetime import datetime
from typing import List
from db import get_session
from models import Order, User, Pizza
from schemas import OrderCreate, OrderUpdate
from utils import verify_access_token

router = APIRouter(tags=['orders'], responses={404: {"description": "Not found"}})


@router.post('/create_order/', response_model=Order)
def create_order(data: OrderCreate, user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
    # Validate pizza_ids
    pizzas = session.exec(select(Pizza).where(Pizza.id.in_(data.pizza_ids), Pizza.status == 'available')).all()
    if not pizzas or len(pizzas) != len(data.pizza_ids):
        raise HTTPException(status_code=400, detail="One or more pizzas are unavailable")

    total_price = sum(pizza.price for pizza in pizzas)

    new_order = Order(
        user_id=user.id,
        pizza_id=",".join(map(str, data.pizza_ids)),
        order_time=data.order_time,
        total_price=total_price
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order


@router.get('/orders/', response_model=List[Order])
def get_orders(user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
    orders = session.exec(select(Order).where(Order.user_id == user.id)).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders


@router.put('/update_order/{order_id}/', response_model=Order)
def update_order(order_id: int, data: OrderUpdate, user: User = Depends(verify_access_token),
                 session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")

    if data.status:
        order.status = data.status
    if data.pizza_ids:
        pizzas = session.exec(select(Pizza).where(Pizza.id.in_(data.pizza_ids), Pizza.status == 'available')).all()
        if not pizzas or len(pizzas) != len(data.pizza_ids):
            raise HTTPException(status_code=400, detail="One or more pizzas are unavailable")
        order.pizza_id = ",".join(map(str, data.pizza_ids))
        order.total_price = sum(pizza.price for pizza in pizzas)
    if data.order_time:
        order.order_time = data.order_time

    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.get('/order/{order_id}/', response_model=Order)
def get_order(order_id: int, user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    return order