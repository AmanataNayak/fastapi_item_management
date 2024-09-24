from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    file_path = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'), nullable=False)

    owner = relationship('User')


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Rating(Base):
    __tablename__ = 'Ratings'
    item_id = Column(Integer, ForeignKey('Item.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    rating = Column(Integer, nullable=False)
