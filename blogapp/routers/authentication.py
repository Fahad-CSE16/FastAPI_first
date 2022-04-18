from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
from hashing import Hash
import models
from datetime import timedelta
from oauth2 import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=['Authentication']
)


@router.post('/token', status_code=status.HTTP_200_OK)
def login_user(request:OAuth2PasswordRequestForm = Depends(), db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(detail=f'Not found for email {request.username}', status_code=status.HTTP_404_NOT_FOUND)
    if Hash.verify_password(request.password, user.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    return {'details':"can't verify"}
