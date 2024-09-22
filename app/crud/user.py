from sqlalchemy.orm import Session
from app import schema, models
from app.utils import get_hash_password
from app.logging_setup import logger


def create_user(db: Session, user: schema.UserCreate):
    new_user = models.User(**user.dict())
    new_user.password = get_hash_password(new_user.password)
    db.add(new_user)
    db.commit()
    logger.info(f'New user create with email:{user.email}')
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()