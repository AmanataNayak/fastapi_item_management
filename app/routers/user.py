from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.CRUD import user as u
from app.database import get_db
from app.schema import UserCreate, UserOut

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return u.create_user(db, user)


@router.get('/{id}', response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return u.get_user_by_id(db, id)
