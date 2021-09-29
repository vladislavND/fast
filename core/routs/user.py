from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.db.dependecy import get_db
from core.crud.user import CRUDUser
from core.models.user import User, UserBase

router = APIRouter()
crud = CRUDUser(User)


@router.get('/users', response_model=UserBase)
def get_users(session: Session = Depends(get_db)):
    return crud.get_all(session)


@router.get('/user/{telegram_id}', response_model=UserBase)
def get_user(telegram_id: int,  session: Session = Depends(get_db)):
    return crud.get_by_telegram_id(session, telegram_id)


@router.post('/user', response_model=User)
def create_user(user: UserBase, session: Session = Depends(get_db)):
    item = crud.create_user(session, user)
    return item









