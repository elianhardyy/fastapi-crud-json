from fastapi import APIRouter, Depends, status, HTTPException, Body, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from schema.user import UserSchema,LoginSchema
from models.user import User
from config.database import db_engine, SessionLocal
from config.templates import templates
from models.user import Base
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from typing import Annotated
import jwt
from datetime import datetime, timedelta
from dotenv import dotenv_values
from utils.jwt import JWTBearer
env = dotenv_values(".env")

Base.metadata.create_all(bind=db_engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

user_route = APIRouter()

def password_hash(password):
    return pwd_context.hash(password)

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)

@user_route.post("/users/",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserSchema,db:Session=Depends(get_db)):
    #u = User()
    user.password = password_hash(user.password)
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@user_route.get("/get-user/",status_code=status.HTTP_200_OK)
async def get_users(db:Session=Depends(get_db)):
    return db.query(User).all()

@user_route.put("/users/{id}",status_code=status.HTTP_200_OK)
async def edit_user(useredit:UserSchema,id:int,db:Session=Depends(get_db)):
    user_old = db.query(User).filter(useredit.id == id).first()
    new_password = password_hash(useredit.password)
    user_old.email = useredit.email
    user_old.password = new_password
    user_old.username = useredit.username
    db.add(user_old)
    db.commit()
    return user_old

users = User()
def check_user(data:LoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@user_route.post("/login")
async def login(user:LoginSchema,db:Session=Depends(get_db)):
    userp = db.query(User).filter(User.email==user.email).first()
    #print(userp.password)
    get_password = userp.password
    
    verify = verify_password(user.password,get_password)
    if not verify:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username"
        )
    payload = {
        "id":userp.id,
        "email":userp.email
    }
    token = jwt.encode(payload,env["SECRETS"])
    print(token)
    return token

@user_route.get("/register",response_class=HTMLResponse)
async def reg(request:Request,user:UserSchema = Form(...)):
    return templates.TemplateResponse("auth/register.html",{"request":request})

async def get_current_user(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="not validate",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,env["SECRETS"],algorithms=['HS256'])
        email:str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = LoginSchema(email=email)
    except:
        raise credentials_exception
    return token_data

async def get_current_active_user(current : Annotated[LoginSchema, Depends(get_current_user)]):
    if current.disabled:
        raise HTTPException(status_code=400, detail="incative")
    return current
    
@user_route.get("/user/me",dependencies=[Depends(JWTBearer())])
async def current_user(user=Depends(JWTBearer()),db:Session=Depends(get_db)):
    payload = jwt.decode(user,env["SECRETS"],algorithms=["HS256"])
    finduser = db.query(User).filter(User.email == payload["email"]).first()
    finduser.is_active = True
    return finduser