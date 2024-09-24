from typing import Optional, List
from fastapi import status, Depends, APIRouter, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.crud import item as i
from app.database import get_db
from app.schema import ItemCreate, Item, ItemOut
from app import oauth2
from app.utils import is_image, create_file_path, item_create_form, delete_file

router = APIRouter(
    prefix='/items',
    tags=['Item']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Item)
async def create_item(item: ItemCreate = item_create_form(ItemCreate), file: UploadFile = File(...),
                      db: Session = Depends(get_db),
                      current_user=Depends(oauth2.get_current_user)):
    if not is_image(file):
        raise HTTPException(status_code=400, detail='File must be a valid image (PNG, JPG).')

    file_path = await create_file_path(file, item.name, item.price, current_user.id)
    return i.create_item(db, item, file_path, current_user)


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
async def update_item(id: int, item_dict: ItemCreate = item_create_form(ItemCreate), file: UploadFile = File(...),
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    if not is_image(file):
        raise HTTPException(status_code=400, detail='File must be a valid image (PNG, JPG).')

    file_path = await create_file_path(file, item_dict.name, item_dict.price, current_user.id)

    return i.update_item(db, id, item_dict, file_path, current_user)
