from typing import List
from fastapi import Depends, status, Response, HTTPException, APIRouter
from schemas import Blog, ShowBlog,  User
from database import get_db
from sqlalchemy.orm import Session
import models
from oauth2 import get_current_user

router = APIRouter(
    prefix="/blog",
    tags=['Blog']
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request:Blog, db:Session= Depends(get_db)):
    new_blog = models.Blog(title=request.title, description = request.description, created_by_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ShowBlog])
def all_blogs(response:Response, db:Session= Depends(get_db), current_user: User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
    return blogs

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def single_blog(id, response:Response, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Not found for id {id}'}
    return blog

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request:Blog, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
    blog.update({'title':request.title, 'description':request.description}, synchronize_session=False)
    db.commit()
    return {'details':"updated"}

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_single_blog(id, response:Response, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
    blog.delete()
    db.commit()
    return {'detail':"Success!"}