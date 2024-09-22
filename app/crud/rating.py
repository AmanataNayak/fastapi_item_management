from sqlalchemy.orm import Session
from app import schema, models
from sqlalchemy import and_
from fastapi import HTTPException, status


def rating(db: Session, rate: schema.Rating, current_user):
    item = db.query(models.Item).filter(models.Item.id == rate.item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Item does not exist')

    rate_data = db.query(models.Rating).filter(
        and_(
            models.Rating.item_id == rate.item_id,
            models.Rating.user_id == current_user.id
        )
    ).first()

    if rate_data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already rated.')
    else:
        new_rate = models.Rating(item_id=rate.item_id, user_id=current_user.id, rating=rate.rating)
        db.add(new_rate)
        db.commit()
        return {
            'message': 'Successfully added a vote'
        }
