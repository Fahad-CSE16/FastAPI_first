from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship('Blog', back_populates='created_by')

class UserInDB(User):
    hashed_password: str

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_by_id = Column(Integer, ForeignKey('users.id'))

    created_by = relationship('User', back_populates='blogs')
