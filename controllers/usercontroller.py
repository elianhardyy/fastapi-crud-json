from fastapi import APIRouter, Depends, status, HTTPException, Body, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config.templates import templates
from schema.user import UserSchema, RegisterSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from config.database import db_engine, SessionLocal
from models.user import User
usercontroller = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
def password_hash(password):
    return pwd_context.hash(password)

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)

@usercontroller.get("/guys",response_class=HTMLResponse)
async def reg(request:Request):
    return templates.TemplateResponse("auth/register.html",{"request":request})

@usercontroller.post("/add-user",response_class=HTMLResponse)
async def add_user(request:Request,
                   username:str=Form(...),
                   email:str = Form(...),
                   password:str = Form(...)
                   ,db:Session=Depends(get_db)):
    password = password_hash(password)
    db_user = User()
    db_user.username = username
    db_user.email = email
    db_user.password = password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return RedirectResponse("/guys")
