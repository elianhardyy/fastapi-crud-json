from pydantic import BaseModel,EmailStr


class UserSchema(BaseModel):
    id:int=0
    name:str
    age:int
    email:str
    address:str

    # class Config:
    #     schema_extra = [
    #         {
    #             "id": 0
    #         }
    #     ]
    