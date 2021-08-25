from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.schemas.user import BaseUser, UsersOut, UserIn, UserOut
from core.db.dependecy import get_db
from core.crud import user as crud

router = APIRouter()


@router.get('/users', response_model=UsersOut)
def get_users(db: Session = Depends(get_db)):
    items = crud.get_users(db)
    return items


@router.get('/user/{telegram_id}', response_model=UserOut)
def get_user(telegram_id: int,  db: Session = Depends(get_db)):
    item = crud.get_user(db, telegram_id)
    return item


@router.post('/user', response_model=BaseUser)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    item = crud.create_user(db, user)
    return item









