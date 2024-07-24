from hashlib import sha256
from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select

from db import get_session
from models import User
from schemas import UserCreate, GetUser, UserUpdate, CreateNewPassword
from utils import create_access_token, verify_access_token, hash_password

router = APIRouter(tags=['user'],
                   responses={404: {"description": "Not found"}})


@router.post('/login/')
async def login_user(response: Response,
                     session: Session = Depends(get_session),
                     data: OAuth2PasswordRequestForm = Depends()
                     ):
    user = session.exec(select(User).where(
        User.email == data.username)).first()
    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401,
                            detail='Incorrect email or password',
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token = create_access_token(data={"sub": user.id})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/register/')
def reg_user(user: UserCreate,
             session: Session = Depends(get_session)
             ):
    temp_user = session.exec(select(User).where(User.email == user.email)).first()
    if temp_user:
        raise HTTPException(status_code=400,
                            detail='Email is busy')
    if user.password != user.complete_password:
        raise HTTPException(status_code=401, detail='Incorrect password')
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email,
                   phone=user.phone,
                   first_name=user.first_name,
                   last_name=user.last_name,
                   surname=user.surname,
                   hash_password=hashed_password,
                   )
    session.add(db_user)
    session.commit()
    raise HTTPException(status_code=200)


@router.post('/token')
def login_user_for_token(response: Response,
                         session: Session = Depends(get_session),
                         data: OAuth2PasswordRequestForm = Depends()
                         ):
    user = session.exec(select(User).where(
        User.email == data.username)).first()  # так как у нас нет username, мы будем использовать email
    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401,
                            detail='Incorrect email or password',
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token = create_access_token(data={"sub": user.id})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/me/')
def user_me(temp_user: User = Depends(verify_access_token)):
    user = GetUser(email=temp_user.email, surname=temp_user.surname)
    return user


@router.get("/users/{email}", response_model=GetUser)
async def get_user(email: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return GetUser(
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        surname=db_user.surname
    )


@router.put("/users/{email}", response_model=GetUser)
async def update_user(email: str, user_update: UserUpdate, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.hash_password = sha256(user_update.password.encode()).hexdigest()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return GetUser(
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        surname=db_user.surname
    )


@router.post("/users/new_password", response_model=GetUser)
async def create_new_password(password_data: CreateNewPassword, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == password_data.email)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.hash_password = sha256(password_data.password.encode()).hexdigest()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return GetUser(
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        surname=db_user.surname
    )