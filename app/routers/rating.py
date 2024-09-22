from fastapi import APIRouter, status, Depends
from app import schema, database, oauth2
from sqlalchemy.orm import Session
from app.CRUD import rating

router = APIRouter(
    prefix='/rate',
    tags=['rate']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def rate(rate: schema.Rating, db: Session = Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):
    return rating.rating(db, rate, current_user)
