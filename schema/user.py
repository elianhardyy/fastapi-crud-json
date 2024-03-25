from pydantic import BaseModel, EmailStr
from datetime import datetime
class UserSchema(BaseModel):
    username:str
    email:EmailStr
    password:str
    created_at:datetime=datetime.now()
    updated_at:datetime=datetime.now()

class RegisterSchema(BaseModel):
    username:str
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class LoginSchema(BaseModel):
    email:EmailStr
    password:str