from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel 

app = FastAPI()


class Blog(BaseModel):
    title : str
    description : str
    is_published : Optional[bool]
    published_at : Optional[str]


@app.get("/")
def home_page():
    return {"data":{
        "Message": "This is Homepage"
    }}

@app.get("/about")
def about_page():
    return {"data":{
        "Message": "This is About page!"
    }}


@app.get("/blogs")
def blog_list():
    return {"data": ["This is blog list page!"]}


@app.get("/blog/unpublished")
def unpublished_blog_list():
    return {"data": ["unpublished blogs"]}


@app.post("/blog/create")
def create_blog(request:Blog):
    return request

@app.get("/blog/{id}")
def blog_list(id : int):
    return {"data": id}


@app.get("/blog/{id}/comments")
def blog_list(id : int):
    return {"data": f'comments of {id}'}

