from fastapi import FastAPI , Depends, status, Response, HTTPException
from . import schemas, models, Hashing
from .database import engine, Base, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()


@app.post('/blog')
def create(request : schemas.Blog, db : Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title,body = request.body,user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog',status_code= status.HTTP_201_CREATED)
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code= status.HTTP_204_NO_CONTENT,detail= "no blogs found")
    return blogs



@app.get('/blog/{id}',status_code= 200,response_model= schemas.ShowBlog)
def show(id :int, response : Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"blog with id {id} not found"}
    return blog


@app.delete('/blog/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id : int, db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message":"deleted from database"}

@app.put('/blog/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id, request : schemas.Blog, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"blog with id {id} not found")
    blog.update(request.title.isnumeri, synchronize_session=False)
    return blog



@app.post('/user',response_model= schemas.ShowUser)
def create_user(request : schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email,password = Hashing.HashClass.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/all-user')
def get_all_users(db : Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

@app.get('/user/{id}',response_model= schemas.User)
def get_user(id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f'User with id {id} not found')
    return user







# @app.get('/blog/{id}')
# def get_blog_details(id : int):
#     if id == 1:
#         return {"message":f"got blog with {id}"}
#     if id == 2:
#         return {"message":f"got blog with {id} 22"}
#     else:
#         return {"error:"}
