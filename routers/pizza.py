from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from typing import List
from db import get_session, engine
from models import User, Pizza, Order
from schemas import AddPizza, GetPizza, PizzaPriceUpdate, PaymentCreate

router = APIRouter(tags=['pizza'],
                   responses={404: {"description": "Not found"}})


@router.post("/pizzas/", response_model=GetPizza)
async def add_pizza(pizza: AddPizza, session: Session = Depends(get_session)):
    db_pizza = Pizza(
        name=pizza.name,
        description=pizza.description,
        price=pizza.price,
        ingredients=','.join(pizza.ingredients)
    )
    session.add(db_pizza)
    session.commit()
    session.refresh(db_pizza)
    return GetPizza(
        name=db_pizza.name,
        description=db_pizza.description,
        price=db_pizza.price,
        ingredients=db_pizza.ingredients.split(',')
    )


@router.get("/pizzas/", response_model=List[GetPizza])
async def get_pizzas(session: Session = Depends(get_session)):
    statement = select(Pizza)
    db_pizzas = session.exec(statement).all()
    return [
        GetPizza(
            name=pizza.name,
            description=pizza.description,
            price=pizza.price,
            ingredients=pizza.ingredients.split(',')
        )
        for pizza in db_pizzas
    ]


@router.put("/pizzas/{pizza_id}/price", response_model=GetPizza)
async def update_pizza_price(pizza_id: int, price_update: PizzaPriceUpdate, session: Session = Depends(get_session)):
    db_pizza = session.get(Pizza, pizza_id)
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    db_pizza.price = price_update.price
    session.add(db_pizza)
    session.commit()
    session.refresh(db_pizza)
    return GetPizza(
        name=db_pizza.name,
        description=db_pizza.description,
        price=db_pizza.price,
        ingredients=db_pizza.ingredients.split(',')
    )