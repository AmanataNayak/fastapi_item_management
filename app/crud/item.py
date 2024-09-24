from fastapi import HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app import schema, models
from app.logging_setup import logger
from typing import Optional
from sqlalchemy import func
from app.utils import delete_file


async def create_item(db: Session, item: schema.ItemCreate, file_path: str, current_user):
    db_item = models.Item(owner_id=current_user.id, file_path=file_path, **item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info('Item created successfully')
    return db_item


def get_item(db: Session, limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    try:
        logger.info('Getting all items')

        query = db.query(models.Item, func.round(func.avg(models.Rating.rating), 2).label('rating')) \
            .join(models.Rating, models.Rating.item_id == models.Item.id, isouter=True) \
            .filter(models.Item.name.contains(search)) \
            .group_by(models.Item.id) \
            .limit(limit) \
            .offset(skip)

        results = query.all()

        formatted_results = [
            {
                'item': schema.Item.from_orm(item),
                'rating': float(rating) if rating is not None else 0
            }
            for item, rating in results
        ]

        return formatted_results

    except Exception as e:
        logger.error(f'Error retrieving items: {e}')
        raise


def get_item_by_id(db: Session, id: int):
    item = db.query(models.Item, func.round(func.avg(models.Rating.rating), 2).label('rating')) \
        .join(models.Rating, models.Rating.item_id == models.Item.id, isouter=True) \
        .group_by(models.Item.id) \
        .filter((models.Item.id == id)) \
        .first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item does not exist')

    formatted_item = {
        'item': item[0],
        'rating': float(item[1]) if item[1] is not None else 0
    }

    return formatted_item


def delete_item(db: Session, id: int, current_user):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        logger.warning(f'Item with id:{id} does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item does not exist')

    if item.owner_id != current_user.id:
        logger.warning(f'Unauthorized user try to delete id:{current_user.id}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this action.')

    delete_file(item.file_path)
    db.delete(item)
    db.commit()
    logger.info(f'Item with id:{id} deleted successfully')
    return item


def update_item(db: Session, id: int, item_dict: schema.ItemCreate, file_path: str, current_user):
    query = db.query(models.Item).filter(models.Item.id == id)
    item = query.first()
    if not item:
        logger.warning(f'Item with id:{id} does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item does not exist')

    if item.owner_id != current_user.id:
        logger.warning(f'Unauthorized user try to update id:{current_user.id}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this action.')
    delete_file(item.file_path)
    item.file_path = file_path
    query.update(item_dict.dict(), synchronize_session=False)
    db.commit()
    logger.info(f'Item with id:{id} updated successfully')
    db.refresh(item)
    return item
