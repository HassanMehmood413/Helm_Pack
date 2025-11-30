from pydantic import BaseModel,validator


class Post(BaseModel):
    id: int
    authur:str
    title: str
    description: str


class PostCreate(BaseModel):
    title: str
    description: str
    authur:str


class UserCreate(BaseModel):
    name: str
    email:str
    password : str

    @validator('password')
    def password_length(cls,v):
        if(len(v) < 6):
            raise ValueError('Password must be at least 6 characters long')
        return v


class UserOut(BaseModel):
    name: str
    email:str


