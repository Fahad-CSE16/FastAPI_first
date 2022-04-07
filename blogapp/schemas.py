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