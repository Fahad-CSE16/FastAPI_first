from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title : str
    description : str


class ShowBlog(BaseModel):
    id: int
    title:str

    class Config:
        orm_mode = True




class User(BaseModel):
    name : str
    email : str
    password : str
class VerifyUser(BaseModel):
    name : str
    password : str


class ShowUser(BaseModel):
    id: int
    name:str
    email:str

    class Config:
        orm_mode = True