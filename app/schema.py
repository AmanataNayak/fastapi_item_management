from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint


class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ItemBase(BaseModel):
    name: str
    price: int


class ItemCreate(ItemBase):
    pass


class Item(ItemCreate):
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class ItemOut(BaseModel):
    item: Item
    rating: float

    class Config:
        form_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Rating(BaseModel):
    item_id: int
    rating: conint(le=5, ge=1)
