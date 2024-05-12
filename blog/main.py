from fastapi import FastAPI , Depends, status, Response, HTTPException
from . import schemas, models, Hashing
from .database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from .database import get_db
from .routers import blog, user

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)



