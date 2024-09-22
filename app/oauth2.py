from datetime import datetime, timedelta
from app import schema, database
import jwt
from jwt.exceptions import PyJWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.CRUD import user
from sqlalchemy.orm import Session
from .config import setting

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expires_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_token


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if not id:
            raise credential_exception
        token_data = schema.TokenData(id=id)

    except PyJWTError:
        raise credential_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized access',
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    token = verify_access_token(token, credential_exception)
    current_user = user.get_user_by_id(db, token.id)
    return current_user
