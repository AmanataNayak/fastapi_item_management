from passlib.context import CryptContext
from fastapi import UploadFile, Form, Depends
import os
from app.schema import ItemCreate

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password, hash_password) -> bool:
    return pwd_context.verify(password, hash_password)


def is_image(file: UploadFile) -> bool:
    valid_extension = ['image/jpeg', 'image/png']
    return file.content_type in valid_extension


async def create_file_path(file: UploadFile, name: str, price: int, id: int) -> str:
    file_extension = file.filename.split('.')[-1]
    file_name = f'{name}_{price}_{id}.{file_extension}'
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, 'wb') as image:
        image.write(await file.read())

    return file_path


def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


def item_create_form(item_create: ItemCreate):

    async def as_form(
            name: str = Form(...),
            price: str = Form(...)
    ):
        return item_create(name=name, price=price)

    return Depends(as_form)
