from fastapi import FastAPI
from schemas import Blog
app = FastAPI()


@app.post("/create")
def create_blog(request:Blog):
    return request
