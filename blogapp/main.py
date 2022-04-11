from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog, ShowBlog, ShowUser, User, VerifyUser
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from hashing import Hash
import models
app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()


@app.post("/create", status_code=status.HTTP_201_CREATED, tags=['blog'])
def create_blog(request:Blog, db:Session= Depends(get_db)):
    new_blog = models.Blog(title=request.title, description = request.description, created_by_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[ShowBlog], tags=['blog'])
def all_blogs(response:Response, db:Session= Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog, tags=['blog'])
def single_blog(id, response:Response, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Not found for id {id}'}
    return blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(id, request:Blog, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
    blog.update({'title':request.title, 'description':request.description}, synchronize_session=False)
    db.commit()
    return {'details':"updated"}

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def delete_single_blog(id, response:Response, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
    blog.delete()
    db.commit()
    return {'detail':"Success!"}


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=ShowUser, tags=['user'])
def create_user(request:User, db:Session= Depends(get_db)):
    new_user = models.User(name=request.name, email = request.email, password = Hash.hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post('/user/verify', status_code=status.HTTP_200_OK, tags=['user'])
def verify_user(request:VerifyUser, response:Response, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.name==request.name).first()
    if not user:
        raise HTTPException(detail=f'Not found for name {request.name}', status_code=status.HTTP_404_NOT_FOUND)
    if Hash.verify_password(request.password, user.password):
        return {'details':"verified"}
    return {'details':"can't verify"}
    

@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser, tags=['user'])
def single_user(id, response:Response, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
    return user