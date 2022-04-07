from fastapi import FastAPI
from schemas import Blog
from database import engine
import models
app = FastAPI()


models.Base.metadata.create_all(engine)

@app.post("/create")
def create_blog(request:Blog):
    return request
