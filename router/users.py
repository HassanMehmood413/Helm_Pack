from fastapi import Depends,HTTPException,APIRouter
from database import engine,get_db
import models,schemas
from models import SQLModel
from sqlmodel import Session


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/users')
def read_post(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

@router.post('/create_user')
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'Added successfully'}



@router.put('/update_user/{id}')
def update_user(id: int,user: schemas.UserCreate,db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id).first()
    if not get_user:
        raise HTTPException(status_code=404,detail='Post Not Found')
    
    for key,value in user.dict().items():
        setattr(get_user,key,value)

    
    db.add(get_user)
    db.commit()
    db.refresh(get_user)

    return {'User Updated Successfully'}



@router.delete('/delete_user/{id}')
def delete_user(id:int,db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id).first()
    if not get_user:
        raise HTTPException(status_code=404,detail='User Not Found')
    
    db.delete(get_user)
    db.commit()

    return {'Deleted Successfully'}




#-------------------
# Using SQLALCHEMY
#-------------------


# from fastapi import FastAPI,Depends
# from database import Base,engine,get_db
# from sqlalchemy.orm import Session
# import models,schemas


# app = FastAPI()

# Base.metadata.create_all(bind=engine)


# @router.get('/posts')
# def read_post(db: Session = Depends(get_db)):
#     all_posts = db.query(models.Post).all()
#     return all_posts

# @router.post('/create_post')
# def create_post(post: schemas.PostCreate, db:Session = Depends(get_db)):
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {'added successfully'}