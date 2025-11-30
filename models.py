#-------------------
# Using SQLMODEL
#-------------------

from sqlmodel import Field,Column,String,Integer,Session,SQLModel
from pydantic import EmailStr


class Post(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    authur: str = Field(nullable=False)


class User(SQLModel,table=True):
    id:int = Field(primary_key=True,nullable=False)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    password : str = Field(nullable=False)



#-------------------
# Using SQLALCHEMY
#-------------------

# from sqlalchemy import Column, String,Integer
# from pydantic import BaseModel,Field
# from database import Base


# class Post(Base):
#     __tablename__ = 'posts'
#     id = Column(Integer,primary_key=True,nullable=False,index=True)
#     authur = Column(String,nullable=False)
#     title = Column(String,nullable=False)
#     description = Column(String,nullable=False)


    
    
    