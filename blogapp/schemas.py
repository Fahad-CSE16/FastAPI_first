from pydantic import BaseModel
from typing import List, Optional


class Blog(BaseModel):
    title : str
    description : str


class ShowBlogs(BaseModel):
    id: int
    title:str
    description:str

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
    blogs : List[ShowBlogs]=[]

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    id: int
    title:str
    created_by : ShowUser

    class Config:
        orm_mode = True