from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()


@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_blog(request:Blog, db:Session= Depends(get_db)):
    new_blog = models.Blog(title=request.title, description = request.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs', status_code=status.HTTP_200_OK)
def all_blogs(response:Response, db:Session= Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def single_blog(id, response:Response, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Not found for id {id}'}
    return blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request:Blog, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
    blog.update({'title':request.title, 'description':request.description}, synchronize_session=False)
    db.commit()
    return {'details':"updated"}

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_single_blog(id, response:Response, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(detail=f'Not found for id {id}', status_code=status.HTTP_404_NOT_FOUND)
    blog.delete()
    db.commit()
    return {'detail':"Success!"}

