from typing import Optional, List
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.CRUD import item as i
from app.database import get_db
from app.schema import ItemCreate, Item, ItemOut
from app import oauth2


router = APIRouter(
    prefix='/items',
    tags=['Item']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    return i.create_item(db, item, current_user)


@router.get('/', response_model=List[ItemOut])
def get_items(limit: int = 100, db: Session = Depends(get_db), skip: int = 0, search: Optional[str] = ""):
    return i.get_item(db, limit, skip, search)


@router.get('/{id}', response_model=ItemOut)
def get_item_by_id(id: int, db: Session = Depends(get_db)):
    return i.get_item_by_id(db, id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return i.delete_item(db, id, current_user)


@router.put('/{id}', response_model=Item)
def update_item(id: int, item_dict: ItemCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return i.update_item(db, id, item_dict, current_user)
