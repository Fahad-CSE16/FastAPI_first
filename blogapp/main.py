from fastapi import FastAPI, Depends
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


@app.post("/create")
def create_blog(request:Blog, db:Session= Depends(get_db)):
    new_blog = models.Blog(title=request.title, description = request.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs')
def all_blogs(db:Session= Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def single_blog(id, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    return blog
