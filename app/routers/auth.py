from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import schema, models, utils, oauth2
from app import schema

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if user_credentials.username == '' or user_credentials.password == '':
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='None value cannot be process')

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    access_token = oauth2.create_access_token(data={
        'user_id': user.id
    })
    return {'access_token': access_token, 'token_type':'bearer'}