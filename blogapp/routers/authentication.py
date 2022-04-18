from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from schemas import Blog, ShowBlog, ShowUser, User, VerifyUser
from database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from hashing import Hash
import models
from datetime import datetime, timedelta
from access_token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/authentication",
    tags=['Authentication']
)


@router.post('/login', status_code=status.HTTP_200_OK)
def login_user(request:VerifyUser, response:Response, db:Session= Depends(get_db)):
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
