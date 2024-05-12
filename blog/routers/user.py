
from fastapi import APIRouter,status ,HTTPException ,Depends ,Response
from ..import models, database,schemas,Hashing
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()



@router.post('/user',response_model= schemas.ShowUser)
def create_user(request : schemas.User, db : Session = Depends(database.get_db)):
    new_user = models.User(name = request.name, email = request.email,password = Hashing.HashClass.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/all-user')
def get_all_users(db : Session = Depends(database.get_db)):
    all_users = db.query(models.User).all()
    return all_users

@router.get('/user/{id}',response_model= schemas.ShowUser)
def get_user(id:int, db : Session = Depends(database.get_db)):
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
