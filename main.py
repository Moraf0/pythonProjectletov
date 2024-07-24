from fastapi import FastAPI, HTTPException, Depends, Response
from sqlmodel import SQLModel, Session, select
from routers import user, payment, pizza, order
from db import get_session, engine

app = FastAPI()
app.include_router(user.router)
app.include_router(payment.router)
app.include_router(pizza.router)
app.include_router(order.router)
SQLModel.metadata.create_all(engine)