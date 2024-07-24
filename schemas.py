from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional


class UserCreate(BaseModel):
    email: EmailStr = Field(default='Email')  # почта
    phone: str = Field(default='+78005553535')
    first_name: str = Field(default='Имя')  # имя
    last_name: str = Field(default='Отчество')  # отчество
    surname: str = Field(default='Фамилия')  # фамилия
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')


class GetUser(BaseModel):
    email: EmailStr = Field(default='Email')  # почта
    first_name: str = Field(default='Имя')  # имя
    last_name: str = Field(default='Отчество')  # отчество
    surname: str = Field(default='Фамилия')  # фамилия


class UserUpdate(BaseModel):
    email: EmailStr = Field(default='Email')
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')


class CreateNewPassword(BaseModel):
    email: EmailStr = Field(default='Email')
    code: str = Field(default='Verify code')
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')


class AddPizza(BaseModel):
    name: str = Field(default='Маргарита')  # название пиццы
    description: Optional[str] = Field(default='Описание пиццы')  # описание пиццы
    price: float = Field(default=500)  # цена пиццы
    ingredients: List[str] = Field(default_factory=list)  # список ингредиентов


class GetPizza(BaseModel):
    name: str = Field(default='Маргарита')  # название пиццы
    description: Optional[str] = Field(default='Описание пиццы')  # описание пиццы
    price: float = Field(default=500)  # цена пиццы
    ingredients: List[str] = Field(default_factory=list)  # список ингредиентов


class PizzaPriceUpdate(BaseModel):
    pizza_id: int
    price: float  # новая цена пиццы


class PaymentCreate(BaseModel):
    card_number: str  # номер карты
    valid_thru_m: datetime = Field(default=datetime.now().month)  # дата валидности банковской карты
    valid_thru_y: datetime = Field(default=datetime.now().year)  # дата валидности банковской карты
    svv: str = Field(default='000')


class OrderCreate(BaseModel):
    pizza_ids: List[int]  # список id пицц
    order_time: Optional[str] = Field(default='10:00')  # время заказа


class OrderUpdate(BaseModel):
    status: Optional[str] = None  # статус заказа
    pizza_ids: Optional[List[int]] = None  # обновленный список id пицц
    order_time: Optional[str] = None  # обновленное время заказа