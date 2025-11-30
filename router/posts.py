from fastapi import Depends,HTTPException,APIRouter
from database import engine,get_db
import models,schemas
from models import SQLModel
from sqlmodel import Session


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/posts')
def read_post(db: Session = Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return all_posts

@router.post('/create_post')
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'added successfully'}



@router.put('/update_post/{id}')
def update_post(id: int,post: schemas.PostCreate,db: Session = Depends(get_db)):
    get_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not get_post:
        raise HTTPException(status_code=404,detail='Post Not Found')
    
    for key,value in post.dict().items():
        setattr(get_post,key,value)

    
    db.add(get_post)
    db.commit()
    db.refresh(get_post)

    return {'Post Updated Successfully'}

@router.delete('/delete_post/{id}')
def delete_post(id:int,db: Session = Depends(get_db)):
    get_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not get_post:
        raise HTTPException(status_code=404,detail='Post Not Found')
    
    db.delete(get_post)
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