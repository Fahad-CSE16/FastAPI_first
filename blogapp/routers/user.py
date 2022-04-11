from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from schemas import Blog, ShowBlog, ShowUser, User, VerifyUser
from database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from hashing import Hash
import models

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
def create_user(request:User, db:Session= Depends(get_db)):
    new_user = models.User(name=request.name, email = request.email, password = Hash.hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/verify', status_code=status.HTTP_200_OK)
def verify_user(request:VerifyUser, response:Response, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.name==request.name).first()
    if not user:
        raise HTTPException(detail=f'Not found for name {request.name}', status_code=status.HTTP_404_NOT_FOUND)
    if Hash.verify_password(request.password, user.password):
        return {'details':"verified"}
    return {'details':"can't verify"}
    

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser)
def single_user(id, response:Response, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
    return user