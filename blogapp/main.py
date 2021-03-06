from fastapi import FastAPI
from database import engine
import models
from routers import user, blog, authentication

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)



@app.get("/")
def root():
    return {"message": "Hello World"}

