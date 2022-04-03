from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title : str
    description : str
    is_published : Optional[bool]
    published_at : Optional[str]