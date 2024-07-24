from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from hashlib import sha256
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    hash_password: str  # хэш пароля
    email: str  # почта
    first_name: str  # имя
    last_name: str  # отчество
    surname: str  # фамилия
    date_reg: datetime = Field(default_factory=datetime.utcnow)  # дата регистрации
    temp_data: str = Field(nullable=True)

    def verify_password(self, password: str) -> bool:
        return self.hash_password == sha256(password.encode()).hexdigest()

    def verify_user(self):
        self.role = 'verify'


class Pizza(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str  # название пиццы
    description: Optional[str] = None  # описание пиццы
    price: float  # цена пиццы
    ingredients: str  # список ингредиентов
    status: str = Field(default='available')  # статус пиццы (available, unavailable)

    def make_unavailable(self):
        self.status = 'unavailable'

    def make_available(self):
        self.status = 'available'


class Order(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key='user.id')  # id пользователя
    pizza_id: str # список id пицц
    order_time: str = Field(default='10:00')  # время заказа
    status: str = Field(default='active')  # статус заказа (active, preparing, completed, cancelled)
    total_price: float

    def prepare(self):
        self.status = 'preparing'

    def complete(self):
        self.status = 'completed'

    def cancel(self):
        self.status = 'cancelled'


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    order_id: int = Field(foreign_key='order.id')  # id заказа
    user_id: int = Field(foreign_key='user.id')  # id пользователя
    amount: float  # сумма оплаты
    card_number: str  # номер карты
    # valid_thru: datetime  # дата валидности банковской карты (можно добавить при необходимости)
    # cvv: str = Field(min_length=3, max_length=3)  # CVV код карты (можно добавить при необходимости)
    payment_date: datetime = Field(default_factory=datetime.utcnow)  # дата оплаты
    status: str = Field(default='waiting')  # статус оплаты (waiting, paid)

    def payment(self):
        self.status = 'payment'