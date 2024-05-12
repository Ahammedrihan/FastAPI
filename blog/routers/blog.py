from fastapi import APIRouter,status ,HTTPException ,Depends ,Response
from ..import models, database,schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/blog',status_code= status.HTTP_201_CREATED)
def all(db : Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code= status.HTTP_204_NO_CONTENT,detail= "no blogs found")
    return blogs

@router.post('/blog')
def create(request : schemas.Blog, db : Session = Depends(database.get_db)):
    new_blog = models.Blog(title = request.title,body = request.body,user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/blog/{id}',status_code= 200,response_model= schemas.ShowBlog)
def show(id :int, response : Response, db : Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"blog with id {id} not found"}
    return blog

@router.delete('/blog/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id : int, db : Session = Depends(database.get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message":"deleted from database"}

@router.put('/blog/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id, request : schemas.Blog, db : Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"blog with id {id} not found")
    blog.update(request.title.isnumeri, synchronize_session=False)
    return blog

