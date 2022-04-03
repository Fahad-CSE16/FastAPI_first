from fastapi import FastAPI

app = FastAPI()

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